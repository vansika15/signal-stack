from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time
import datetime

from ..database import get_db
from ..models.company import Company
from ..models.competitor import Competitor
from ..schemas.competitor import CompetitorResponse, CompetitorCreate
from ..services.ai_service import AIService

router = APIRouter(prefix="/api/competitors", tags=["Competitor Intelligence"])

@router.get("/{company_id}", response_model=List[CompetitorResponse])
def get_competitors(company_id: str, db: Session = Depends(get_db)):
    return db.query(Competitor).filter(Competitor.company_id == company_id).all()

@router.post("/{company_id}", response_model=CompetitorResponse)
def add_competitor(company_id: str, req: CompetitorCreate, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    cid = f"comp_{int(time.time()*1000)}"
    competitor = Competitor(
        id=cid,
        company_id=company_id,
        name=req.name,
        website=req.website,
        tier=req.tier,
        market_focus=req.market_focus,
        key_strengths=req.key_strengths,
        vulnerabilities=req.vulnerabilities,
        monitored=req.monitored,
        discovery_method="manual",
        created_at=datetime.datetime.utcnow()
    )
    db.add(competitor)
    db.commit()
    db.refresh(competitor)
    return competitor

@router.post("/{company_id}/discover", response_model=List[CompetitorResponse])
def discover_competitors(company_id: str, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    discovered = AIService.discover_competitors({
        "name": comp.name,
        "industry": comp.industry,
        "website": comp.website,
        "description": comp.description
    })

    created = []
    for d in discovered:
        # Check if already exists
        exists = db.query(Competitor).filter(
            Competitor.company_id == company_id,
            Competitor.name.ilike(d["name"])
        ).first()
        if not exists:
            cid = f"comp_{int(time.time()*1000)}_{abs(hash(d['name'])) % 1000}"
            competitor = Competitor(
                id=cid,
                company_id=company_id,
                name=d["name"],
                website=d.get("website"),
                tier=d.get("tier", "Direct"),
                market_focus=d.get("market_focus"),
                key_strengths=d.get("key_strengths"),
                vulnerabilities=d.get("vulnerabilities"),
                monitored=True,
                discovery_method="ai_discovered",
                created_at=datetime.datetime.utcnow()
            )
            db.add(competitor)
            created.append(competitor)
    db.commit()
    for c in created:
        db.refresh(c)
    return db.query(Competitor).filter(Competitor.company_id == company_id).all()

@router.delete("/{competitor_id}")
def delete_competitor(competitor_id: str, db: Session = Depends(get_db)):
    comp = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Competitor not found")
    db.delete(comp)
    db.commit()
    return {"message": "Competitor removed successfully"}
