import os
import sys
import json
import time
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.database import SessionLocal
from app.models.company import Company
from app.models.source import Source
from app.models.crawl_history import CrawlHistory
from app.models.intelligence import IntelligenceItem
from app.services.crawler_service import CrawlerService

def main():
    db = SessionLocal()
    print("=" * 80)
    print("SIGNAL STACK – GENUINE SOURCE & CRAWLER VERIFICATION AUDIT")
    print("=" * 80)

    # 1. Fetch MeetUniversity Sources
    mu_sources = db.query(Source).filter(Source.company_id == "meetuniversity").order_by(Source.created_at.asc()).all()
    print(f"\n1. RETRIEVED {len(mu_sources)} MEETUNIVERSITY SOURCES FROM DATABASE:\n")
    
    source_list = []
    for idx, s in enumerate(mu_sources, 1):
        source_list.append({
            "index": idx,
            "id": s.id,
            "name": s.name,
            "url": s.url,
            "source_type": s.source_type,
            "approved_status": s.approved_status,
            "relevance": s.relevance_explanation
        })
        print(f"[{idx:02d}] {s.name}")
        print(f"     URL: {s.url}")
        print(f"     Type: {s.source_type} | Status: {s.approved_status}")
        print(f"     Relevance: {s.relevance_explanation[:110]}...")

    # Record existing intelligence IDs before crawling to distinguish seeded from crawled
    existing_intel = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "meetuniversity").all()
    seeded_ids = set(item.id for item in existing_intel)
    print(f"\nBaseline Seeded Intelligence Records Count: {len(seeded_ids)}")

    # 2 & 4. Run the Actual Crawler across all approved sources
    print("\n" + "=" * 80)
    print("2. RUNNING LIVE WEB CRAWLER ON MONITORED PUBLIC SOURCES...")
    print("=" * 80 + "\n")

    crawl_results = []
    for idx, s in enumerate(mu_sources, 1):
        print(f"--> [{idx:02d}/{len(mu_sources)}] Crawling: {s.name} ({s.url})...")
        t0 = time.time()
        res = CrawlerService.crawl_source(db, s)
        elapsed = round(time.time() - t0, 2)
        res["elapsed_s"] = elapsed
        crawl_results.append(res)
        print(f"    Status: {res.get('status_code')} | Health: {res.get('health_status')} | Diff: {res.get('has_changes')} | New Signals: {res.get('signals_extracted')} ({elapsed}s)")

    # 5. Aggregate Results
    successful = [r for r in crawl_results if r.get("status_code") and 200 <= r.get("status_code") < 400]
    failed_or_blocked = [r for r in crawl_results if not r.get("status_code") or r.get("status_code") >= 400]
    total_signals_extracted = sum(r.get("signals_extracted", 0) for r in crawl_results)

    print("\n" + "=" * 80)
    print("3. CRAWLER HARVEST & ACCESSIBILITY SUMMARY")
    print("=" * 80)
    print(f"Total Sources Monitored: {len(mu_sources)}")
    print(f"Successfully Fetched (HTTP 200/3xx): {len(successful)}")
    print(f"Degraded/Blocked/Unreachable: {len(failed_or_blocked)}")
    print(f"Total New Intelligence Signals Extracted: {total_signals_extracted}")

    if failed_or_blocked:
        print("\nDetails on Degraded / Unreachable Sources:")
        for fb in failed_or_blocked:
            print(f"  • {fb.get('source_name')} ({fb.get('status_code') or 'TIMEOUT/ERR'}): {fb.get('error_details')}")

    # 6. Verify SHA-256 Change Detection & Deduplication Test
    print("\n" + "=" * 80)
    print("4. VERIFYING SHA-256 CHANGE DETECTION & DEDUPLICATION (2nd Pass Test)")
    print("=" * 80)
    
    # Pick the first 3 successful sources and crawl them immediately a second time
    test_sources = [s for s in mu_sources if s.last_status_code == 200][:3]
    for ts in test_sources:
        stored_hash = ts.content_hash
        print(f"\nTesting Change Detection on: {ts.name}")
        print(f"  Current SHA-256 Content Hash: {stored_hash[:24]}...")
        re_crawl = CrawlerService.crawl_source(db, ts)
        print(f"  Re-crawl Result: has_changes={re_crawl.get('has_changes')}, signals_extracted={re_crawl.get('signals_extracted')}")
        assert re_crawl.get('has_changes') is False, f"Expected has_changes=False on unchanged page for {ts.name}"
        assert re_crawl.get('signals_extracted') == 0, f"Expected 0 new signals (no duplicates) on unchanged page for {ts.name}"
        print(f"  ✔ Verified: Content hash matches! No duplicate signals created.")

    # 7. Intelligence Records Inspection: Distinguish Seeded vs. Crawled
    all_current_intel = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "meetuniversity").order_by(IntelligenceItem.discovery_date.desc()).all()
    
    crawled_intel = [item for item in all_current_intel if item.id not in seeded_ids]
    seeded_intel = [item for item in all_current_intel if item.id in seeded_ids]

    print("\n" + "=" * 80)
    print(f"5. DATABASE INTELLIGENCE RECORDS BREAKDOWN")
    print(f"   Seeded Baseline Records: {len(seeded_intel)}")
    print(f"   Genuinely Crawled Records: {len(crawled_intel)}")
    print("=" * 80)

    if crawled_intel:
        print("\nGENUINELY CRAWLED INTELLIGENCE SIGNALS FROM LIVE WEBPAGES:")
        for idx, ci in enumerate(crawled_intel, 1):
            print(f"\n--- [CRAWLED SIGNAL #{idx}] ---")
            print(f"ID: {ci.id}")
            print(f"Category: {ci.category} | Nature: {ci.nature} | Urgency: {ci.urgency}")
            print(f"Headline: {ci.headline}")
            print(f"Summary: {ci.summary[:200]}...")
            print(f"Evidence Excerpt: {ci.evidence}")
            print(f"Original URL: {ci.original_url}")
            print(f"Publication / Crawled Date: {ci.publication_date}")
            print(f"Calculated Score: {ci.ranking_score}/100")
            print(f"Ranking Breakdown: {json.dumps(ci.ranking_breakdown.get('components', {}), indent=2)}")

    print("\nSEEDED BASELINE STRATEGIC SIGNALS (Pre-seeded for Demonstration):")
    for idx, si in enumerate(seeded_intel[:4], 1):
        print(f"  [{idx}] {si.headline} ({si.category} - Score: {si.ranking_score})")

    db.close()
    print("\n" + "=" * 80)
    print("AUDIT EXECUTION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
