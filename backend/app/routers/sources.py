from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time
import datetime

from ..database import get_db
from ..models.company import Company
from ..models.source import Source
from ..schemas.source import SourceResponse, SourceCreate, SourceStatusUpdate, SourceHealthAuditItem
from ..services.ai_service import AIService
from ..services.crawler_service import CrawlerService

router = APIRouter(prefix="/api/sources", tags=["Source Manager"])

@router.get("/{company_id}", response_model=List[SourceResponse])
def get_sources(company_id: str, db: Session = Depends(get_db)):
    return db.query(Source).filter(Source.company_id == company_id).order_by(Source.created_at.asc()).all()

@router.post("/{company_id}", response_model=SourceResponse)
def add_source(company_id: str, req: SourceCreate, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    sid = f"src_{int(time.time()*1000)}"
    source = Source(
        id=sid,
        company_id=company_id,
        name=req.name,
        url=req.url,
        source_type=req.source_type,
        relevance_explanation=req.relevance_explanation,
        approved_status=req.approved_status,
        health_status="healthy",
        crawl_frequency_hours=24,
        created_at=datetime.datetime.utcnow()
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source

@router.post("/{company_id}/discover", response_model=List[SourceResponse])
def discover_sources(company_id: str, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    recommendations = AIService.recommend_sources({"name": comp.name, "industry": comp.industry, "website": comp.website})
    for r in recommendations:
        existing = db.query(Source).filter(
            Source.company_id == company_id,
            Source.url == r["url"]
        ).first()
        if not existing:
            sid = f"src_{int(time.time()*1000)}_{abs(hash(r['url'])) % 1000}"
            src = Source(
                id=sid,
                company_id=company_id,
                name=r["name"],
                url=r["url"],
                source_type=r["source_type"],
                relevance_explanation=r["relevance_explanation"],
                approved_status=r.get("approved_status", "approved"),
                health_status="healthy",
                crawl_frequency_hours=24,
                created_at=datetime.datetime.utcnow()
            )
            db.add(src)
    db.commit()
    return db.query(Source).filter(Source.company_id == company_id).all()

@router.put("/{source_id}/status", response_model=SourceResponse)
def update_source_status(source_id: str, req: SourceStatusUpdate, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    source.approved_status = req.approved_status
    db.commit()
    db.refresh(source)
    return source

@router.delete("/{source_id}")
def delete_source(source_id: str, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(source)
    db.commit()
    return {"message": "Source removed successfully"}

@router.post("/audit", response_model=List[SourceHealthAuditItem])
def audit_sources(company_id: str = None, db: Session = Depends(get_db)):
    """Triggers real source-health audit checking availability and status codes"""
    results = CrawlerService.audit_sources_health(db, company_id)
    return results
