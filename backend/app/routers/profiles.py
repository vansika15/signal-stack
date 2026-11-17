from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime

from ..database import get_db
from ..models.company import Company, CompanyProfile
from ..schemas.company import CompanyProfileResponse
from ..services.ai_service import AIService

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])

@router.get("/{company_id}", response_model=CompanyProfileResponse)
def get_company_profile(company_id: str, db: Session = Depends(get_db)):
    profile = db.query(CompanyProfile).filter(CompanyProfile.company_id == company_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Company profile not found")
    return profile

@router.post("/{company_id}/generate", response_model=CompanyProfileResponse)
def generate_profile(company_id: str, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    res = AIService.research_company(comp.website, comp.name)
    profile = db.query(CompanyProfile).filter(CompanyProfile.company_id == company_id).first()
    if not profile:
        profile = CompanyProfile(id=f"prof_{company_id}", company_id=company_id)
        db.add(profile)

    profile.business_model = res.get("business_model")
    profile.value_proposition = res.get("value_proposition")
    profile.pricing_tier = res.get("pricing_tier")
    profile.strategic_priorities = res.get("strategic_priorities", [])
    profile.key_differentiators = res.get("key_differentiators", [])
    profile.risks_and_challenges = res.get("risks_and_challenges", [])
    profile.updated_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(profile)
    return profile
