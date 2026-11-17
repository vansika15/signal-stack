from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import datetime

from ..database import get_db
from ..models.company import Company, CompanyProfile
from ..schemas.company import (
    CompanyResponse, CompanyCreate, CompanyUpdate, CompanyResearchRequest, CompanyProfileResponse
)
from ..services.ai_service import AIService

router = APIRouter(prefix="/api/companies", tags=["Companies"])

@router.get("", response_model=List[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).order_by(Company.created_at.asc()).all()

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: str, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")
    return comp

@router.post("/research")
def research_company(req: CompanyResearchRequest):
    data = AIService.research_company(req.website, req.company_name)
    return data

@router.post("", response_model=CompanyResponse)
def create_company(req: CompanyCreate, db: Session = Depends(get_db)):
    cid = req.id or req.name.lower().replace(" ", "").replace(".", "")
    existing = db.query(Company).filter(Company.id == cid).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company with this ID already exists")

    new_comp = Company(
        id=cid,
        name=req.name,
        website=req.website,
        domain=req.domain,
        industry=req.industry,
        description=req.description,
        target_audience=req.target_audience,
        primary_markets=req.primary_markets,
        business_context=req.business_context,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_comp)

    # Automatically generate initial profile
    res = AIService.research_company(req.website, req.name)
    profile = CompanyProfile(
        id=f"prof_{cid}",
        company_id=cid,
        business_model=res.get("business_model", ""),
        value_proposition=res.get("value_proposition", ""),
        pricing_tier=res.get("pricing_tier", "Enterprise"),
        strategic_priorities=res.get("strategic_priorities", []),
        key_differentiators=res.get("key_differentiators", []),
        risks_and_challenges=res.get("risks_and_challenges", []),
        tech_stack_summary=f"Automated intelligence profile for {req.name}",
        generated_by="ai_heuristic"
    )
    db.add(profile)
    db.commit()
    db.refresh(new_comp)
    return new_comp

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: str, req: CompanyUpdate, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    if req.name is not None: comp.name = req.name
    if req.website is not None: comp.website = req.website
    if req.industry is not None: comp.industry = req.industry
    if req.description is not None: comp.description = req.description
    if req.target_audience is not None: comp.target_audience = req.target_audience
    if req.primary_markets is not None: comp.primary_markets = req.primary_markets
    if req.business_context is not None: comp.business_context = req.business_context

    comp.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(comp)
    return comp

@router.delete("/{company_id}")
def delete_company(company_id: str, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(comp)
    db.commit()
    return {"message": f"Company {company_id} deleted successfully"}
