from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import time
import datetime

from ..database import get_db
from ..models.company import Company
from ..models.intelligence import IntelligenceItem
from ..schemas.intelligence import IntelligenceResponse, IntelligenceCreate
from ..services.ranking_service import RankingService

router = APIRouter(prefix="/api/intelligence", tags=["Signal Stack & Intelligence Feed"])

@router.get("/{company_id}", response_model=List[IntelligenceResponse])
def get_intelligence(
    company_id: str,
    category: Optional[str] = Query(None, description="Customer Intelligence, Competitor Intelligence, Market Intelligence, Internal Intelligence"),
    search: Optional[str] = Query(None, description="Search keyword in headline/summary"),
    impact: Optional[str] = Query(None, description="High, Medium, Low"),
    urgency: Optional[str] = Query(None, description="Immediate, Short-Term, Medium-Term, Watchlist"),
    verification: Optional[str] = Query(None, description="Verified, Pending Verification, Unverified"),
    include_archived: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == company_id)

    if not include_archived:
        query = query.filter(IntelligenceItem.is_archived == False)

    if category and category != "All":
        query = query.filter(IntelligenceItem.category == category)

    if impact:
        query = query.filter(IntelligenceItem.business_impact == impact)

    if urgency:
        query = query.filter(IntelligenceItem.urgency == urgency)

    if verification:
        query = query.filter(IntelligenceItem.verification_status == verification)

    if search:
        term = f"%{search}%"
        query = query.filter((IntelligenceItem.headline.ilike(term)) | (IntelligenceItem.summary.ilike(term)))

    # Order by ranking score descending (highest priority signals first)
    return query.order_by(IntelligenceItem.ranking_score.desc()).all()

@router.post("/{company_id}", response_model=IntelligenceResponse)
def create_intelligence(company_id: str, req: IntelligenceCreate, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    # Run explainable ranking algorithm
    ranking = RankingService.calculate_ranking(
        strategic_relevance=req.strategic_relevance,
        business_impact=req.business_impact,
        urgency=req.urgency,
        source_reliability=req.source_reliability,
        evidence_strength=req.evidence_strength,
        verification_status=req.verification_status,
        publication_date=datetime.datetime.utcnow(),
        discovery_date=datetime.datetime.utcnow()
    )

    item = IntelligenceItem(
        id=f"intel_{int(time.time()*1000)}",
        company_id=company_id,
        source_id=req.source_id,
        competitor_id=req.competitor_id,
        category=req.category,
        headline=req.headline,
        summary=req.summary,
        evidence=req.evidence,
        original_url=req.original_url,
        publication_date=datetime.datetime.utcnow(),
        discovery_date=datetime.datetime.utcnow(),
        verification_status=req.verification_status,
        source_reliability=req.source_reliability,
        evidence_strength=req.evidence_strength,
        strategic_relevance=req.strategic_relevance,
        business_impact=req.business_impact,
        nature=req.nature,
        urgency=req.urgency,
        recommended_action=req.recommended_action,
        ranking_score=ranking["score"],
        ranking_breakdown=ranking["breakdown"],
        is_archived=False,
        created_at=datetime.datetime.utcnow()
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{item_id}/ranking-breakdown")
def get_ranking_breakdown(item_id: str, db: Session = Depends(get_db)):
    item = db.query(IntelligenceItem).filter(IntelligenceItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Intelligence item not found")

    return {
        "id": item.id,
        "headline": item.headline,
        "ranking_score": item.ranking_score,
        "breakdown": item.ranking_breakdown,
        "inputs": {
            "strategic_relevance": item.strategic_relevance,
            "business_impact": item.business_impact,
            "urgency": item.urgency,
            "source_reliability": item.source_reliability,
            "evidence_strength": item.evidence_strength,
            "verification_status": item.verification_status
        }
    }

@router.put("/{item_id}/archive", response_model=IntelligenceResponse)
def toggle_archive(item_id: str, db: Session = Depends(get_db)):
    item = db.query(IntelligenceItem).filter(IntelligenceItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Intelligence item not found")
    item.is_archived = not item.is_archived
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_intelligence(item_id: str, db: Session = Depends(get_db)):
    item = db.query(IntelligenceItem).filter(IntelligenceItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Intelligence item not found")
    db.delete(item)
    db.commit()
    return {"message": "Intelligence item deleted"}
