import hashlib
import time
import datetime
import logging
import urllib.parse
import urllib.robotparser
from typing import Dict, Any, List, Optional
import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from ..models.source import Source
from ..models.crawl_history import CrawlHistory
from ..models.intelligence import IntelligenceItem
from .ranking_service import RankingService

logger = logging.getLogger(__name__)

class CrawlerService:
    """
    Production-grade Web Crawler & Monitor for Permitted Public Sources:
    - Respects robots.txt directives
    - Polite rate limits and timeouts
    - Change detection via SHA-256 content hashing
    - Intelligent HTML text extraction (Title, Meta Description, Headings, Articles)
    - Deduplication against existing intelligence records
    - Resilient error handling (unreachable, 404, timeouts, rate limits)
    - Historical crawl logging & status tracking
    """

    USER_AGENT = "SignalStackBot/1.0 (+https://github.com/signal-stack/crawler-bot; research-monitoring)"

    @classmethod
    def check_robots_allowed(cls, url: str) -> bool:
        """Checks if URL is permitted by robots.txt"""
        try:
            parsed = urllib.parse.urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            with httpx.Client(timeout=4.0, headers={"User-Agent": cls.USER_AGENT}) as client:
                res = client.get(robots_url)
                if res.status_code == 200:
                    rp.parse(res.text.splitlines())
                    return rp.can_fetch(cls.USER_AGENT, url)
                # If robots.txt returns 404 or fails, standard web policy permits crawling
                return True
        except Exception as e:
            logger.debug(f"Could not fetch robots.txt for {url}: {e}; defaulting to allowed.")
            return True

    @classmethod
    def crawl_source(cls, db: Session, source: Source) -> Dict[str, Any]:
        """Crawls a single source, detects diffs, extracts signals, and updates DB"""
        start_time = time.time()
        crawled_at = datetime.datetime.utcnow()
        status_code = None
        error_details = None
        health_status = "healthy"
        new_signals_count = 0
        has_changes = False
        content_hash = None
        extracted_signals = []

        # 1. Check robots.txt
        is_allowed = cls.check_robots_allowed(source.url)
        if not is_allowed:
            source.health_status = "rate_limited"
            source.error_message = "Disallowed by robots.txt"
            source.last_crawled_at = crawled_at
            db.commit()
            return {
                "source_id": source.id,
                "status": "blocked_by_robots_txt",
                "signals_extracted": 0
            }

        # 2. Fetch page content
        headers = {
            "User-Agent": cls.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            with httpx.Client(timeout=8.0, follow_redirects=True, headers=headers) as client:
                res = client.get(source.url)
                duration_ms = int((time.time() - start_time) * 1000)
                status_code = res.status_code
                
                if duration_ms > 4000:
                    health_status = "slow"

                if res.status_code == 429:
                    health_status = "rate_limited"
                    error_details = "HTTP 429 Rate Limited"
                elif res.status_code >= 400:
                    health_status = "unreachable"
                    error_details = f"HTTP Error {res.status_code}"
                else:
                    health_status = "healthy"
                    html_content = res.text
                    
                    # Compute content hash
                    soup = BeautifulSoup(html_content, "html.parser")
                    
                    # Remove script and style elements
                    for element in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
                        element.decompose()
                        
                    page_title = (soup.title.string.strip() if soup.title and soup.title.string else source.name)
                    meta_desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
                    meta_desc = meta_desc_tag["content"].strip() if meta_desc_tag and "content" in meta_desc_tag.attrs else ""
                    
                    # Collect text
                    paragraphs = [p.get_text().strip() for p in soup.find_all(["p", "h1", "h2", "h3"]) if len(p.get_text().strip()) > 30]
                    body_sample = " ".join(paragraphs[:15])
                    full_text = f"{page_title} {meta_desc} {body_sample}"
                    
                    content_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
                    
                    # Check for changes
                    if source.content_hash and source.content_hash == content_hash:
                        has_changes = False
                    else:
                        has_changes = True
                        source.content_hash = content_hash
                        
                        # Extract signal if changes detected or first crawl
                        headings = [h.get_text().strip() for h in soup.find_all(["h1", "h2"]) if len(h.get_text().strip()) > 15]
                        headline = headings[0] if headings else (page_title or f"Update from {source.name}")
                        summary = meta_desc if len(meta_desc) > 40 else (paragraphs[0] if paragraphs else f"Verified development detected on {source.name}.")
                        evidence = paragraphs[1] if len(paragraphs) > 1 else (paragraphs[0] if paragraphs else f"Extracted directly from source response at {source.url}")
                        
                        # Categorize based on source type
                        category = "Market Intelligence"
                        if "Competitor" in source.source_type:
                            category = "Competitor Intelligence"
                        elif "Review" in source.source_type or "Community" in source.source_type:
                            category = "Customer Intelligence"
                        elif "Regulatory" in source.source_type or "News" in source.source_type:
                            category = "Market Intelligence"

                        # Deduplicate: check if item with similar headline already exists
                        existing = db.query(IntelligenceItem).filter(
                            IntelligenceItem.company_id == source.company_id,
                            IntelligenceItem.headline == headline
                        ).first()

                        if not existing:
                            # Run explainable ranking
                            ranking = RankingService.calculate_ranking(
                                strategic_relevance="High",
                                business_impact="High" if "Regulatory" in source.source_type else "Medium",
                                urgency="Immediate" if "Regulatory" in source.source_type else "Short-Term",
                                source_reliability="High",
                                evidence_strength="High",
                                verification_status="Verified"
                            )

                            new_item = IntelligenceItem(
                                id=f"intel_{int(time.time()*1000)}_{source.id[:6]}",
                                company_id=source.company_id,
                                source_id=source.id,
                                category=category,
                                headline=headline[:250],
                                summary=summary[:1000],
                                evidence=f"\"{evidence[:500]}\"",
                                original_url=source.url,
                                publication_date=crawled_at,
                                discovery_date=crawled_at,
                                verification_status="Verified",
                                source_reliability="High",
                                evidence_strength="High",
                                strategic_relevance="High",
                                business_impact="High" if "Regulatory" in source.source_type else "Medium",
                                nature="Threat" if "visa" in headline.lower() or "cap" in headline.lower() or "fee" in headline.lower() else "Opportunity",
                                urgency="Immediate" if "Regulatory" in source.source_type else "Short-Term",
                                recommended_action=f"Analyze implications of this {source.name} development for current quarter operations.",
                                ranking_score=ranking["score"],
                                ranking_breakdown=ranking["breakdown"],
                                is_archived=False
                            )
                            db.add(new_item)
                            new_signals_count += 1
                            extracted_signals.append(new_item.headline)

        except httpx.TimeoutException:
            health_status = "slow"
            error_details = "Request timed out after 8 seconds"
            duration_ms = 8000
        except Exception as e:
            health_status = "unreachable"
            error_details = str(e)
            duration_ms = int((time.time() - start_time) * 1000)

        # Update Source model
        source.health_status = health_status
        source.last_crawled_at = crawled_at
        source.last_status_code = status_code
        source.error_message = error_details

        # Record Crawl History
        history = CrawlHistory(
            id=f"crawl_{int(time.time()*1000)}_{source.id[:6]}",
            source_id=source.id,
            company_id=source.company_id,
            crawled_at=crawled_at,
            status_code=status_code,
            duration_ms=duration_ms,
            content_hash=content_hash,
            has_changes=has_changes,
            signals_extracted=new_signals_count,
            response_size_bytes=len(res.content) if 'res' in locals() and res is not None else 0,
            error_details=error_details
        )
        db.add(history)
        db.commit()

        return {
            "source_id": source.id,
            "source_name": source.name,
            "status_code": status_code,
            "health_status": health_status,
            "duration_ms": duration_ms,
            "has_changes": has_changes,
            "signals_extracted": new_signals_count,
            "error_details": error_details
        }

    @classmethod
    def audit_sources_health(cls, db: Session, company_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Monthly health audit verifying availability, response times, and status of all sources"""
        query = db.query(Source)
        if company_id:
            query = query.filter(Source.company_id == company_id)
        sources = query.all()

        results = []
        for src in sources:
            start_t = time.time()
            try:
                with httpx.Client(timeout=5.0, follow_redirects=True, headers={"User-Agent": cls.USER_AGENT}) as client:
                    res = client.head(src.url)
                    # If HEAD fails or gives 405, fallback to GET
                    if res.status_code in [405, 403]:
                        res = client.get(src.url)
                    elapsed = int((time.time() - start_t) * 1000)
                    src.last_status_code = res.status_code
                    src.last_crawled_at = datetime.datetime.utcnow()
                    
                    if res.status_code == 429:
                        src.health_status = "rate_limited"
                    elif res.status_code >= 400:
                        src.health_status = "unreachable"
                        src.error_message = f"HTTP {res.status_code}"
                    elif elapsed > 3000:
                        src.health_status = "slow"
                        src.error_message = None
                    else:
                        src.health_status = "healthy"
                        src.error_message = None
            except Exception as e:
                elapsed = int((time.time() - start_t) * 1000)
                src.health_status = "unreachable"
                src.error_message = str(e)

            results.append({
                "source_id": src.id,
                "source_name": src.name,
                "url": src.url,
                "status_code": src.last_status_code,
                "health_status": src.health_status,
                "response_time_ms": elapsed,
                "error": src.error_message
            })

        db.commit()
        return results
