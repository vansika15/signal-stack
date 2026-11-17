from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time
import datetime

from ..database import get_db
from ..models.company import Company
from ..models.document import InternalDocument
from ..models.intelligence import IntelligenceItem
from ..schemas.document import InternalDocumentResponse, InternalDocumentCreate
from ..services.ai_service import AIService
from ..services.ranking_service import RankingService

router = APIRouter(prefix="/api/internal-docs", tags=["Internal Intelligence"])

@router.get("/{company_id}", response_model=List[InternalDocumentResponse])
def get_documents(company_id: str, db: Session = Depends(get_db)):
    return db.query(InternalDocument).filter(InternalDocument.company_id == company_id).order_by(InternalDocument.created_at.desc()).all()

@router.post("/{company_id}", response_model=InternalDocumentResponse)
def ingest_document(company_id: str, req: InternalDocumentCreate, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    # Extract actionable signals from the document content using AI
    signals = AIService.analyze_internal_document(req.title, req.doc_type, req.content, comp.name)

    doc_id = f"doc_{int(time.time()*1000)}"
    doc = InternalDocument(
        id=doc_id,
        company_id=company_id,
        title=req.title,
        doc_type=req.doc_type,
        content=req.content,
        extracted_signals_count=len(signals),
        created_at=datetime.datetime.utcnow()
    )
    db.add(doc)

    # Add each extracted signal into the IntelligenceItem table under "Internal Intelligence"
    for s in signals:
        ranking = RankingService.calculate_ranking(
            strategic_relevance=s.get("strategic_relevance", "High"),
            business_impact=s.get("business_impact", "High"),
            urgency=s.get("urgency", "Immediate"),
            source_reliability="High",
            evidence_strength="High",
            verification_status="Verified"
        )
        item = IntelligenceItem(
            id=f"intel_{int(time.time()*1000)}_{abs(hash(s['headline'])) % 1000}",
            company_id=company_id,
            category="Internal Intelligence",
            headline=s["headline"],
            summary=s["summary"],
            evidence=s["evidence"],
            original_url=None,
            publication_date=datetime.datetime.utcnow(),
            discovery_date=datetime.datetime.utcnow(),
            verification_status="Verified",
            source_reliability="High",
            evidence_strength="High",
            strategic_relevance=s.get("strategic_relevance", "High"),
            business_impact=s.get("business_impact", "High"),
            nature=s.get("nature", "Opportunity"),
            urgency=s.get("urgency", "Immediate"),
            recommended_action=s["recommended_action"],
            ranking_score=ranking["score"],
            ranking_breakdown=ranking["breakdown"],
            is_archived=False,
            created_at=datetime.datetime.utcnow()
        )
        db.add(item)

    db.commit()
    db.refresh(doc)
    return doc
