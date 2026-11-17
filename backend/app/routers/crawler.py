from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database import get_db
from ..models.source import Source
from ..models.crawl_history import CrawlHistory
from ..services.crawler_service import CrawlerService

router = APIRouter(prefix="/api/crawler", tags=["Web Crawler"])

@router.post("/crawl/{source_id}")
def crawl_single_source(source_id: str, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    res = CrawlerService.crawl_source(db, source)
    return res

@router.post("/crawl-all/{company_id}")
def crawl_all_approved_sources(company_id: str, db: Session = Depends(get_db)):
    sources = db.query(Source).filter(
        Source.company_id == company_id,
        Source.approved_status == "approved"
    ).all()

    results = []
    for src in sources:
        crawl_res = CrawlerService.crawl_source(db, src)
        results.append(crawl_res)

    total_extracted = sum([r.get("signals_extracted", 0) for r in results])
    return {
        "sources_crawled": len(sources),
        "total_new_signals_extracted": total_extracted,
        "results": results
    }

@router.get("/history/{company_id}")
def get_crawl_history(company_id: str, db: Session = Depends(get_db)):
    history = db.query(CrawlHistory).filter(
        CrawlHistory.company_id == company_id
    ).order_by(CrawlHistory.crawled_at.desc()).limit(50).all()

    return [
        {
            "id": h.id,
            "source_id": h.source_id,
            "source_name": h.source.name if h.source else "Unknown",
            "crawled_at": h.crawled_at,
            "status_code": h.status_code,
            "duration_ms": h.duration_ms,
            "has_changes": h.has_changes,
            "signals_extracted": h.signals_extracted,
            "response_size_bytes": h.response_size_bytes,
            "error_details": h.error_details
        }
        for h in history
    ]
