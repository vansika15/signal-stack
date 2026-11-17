from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    website: str
    domain: str
    industry: str
    description: Optional[str] = None
    target_audience: Optional[str] = None
    primary_markets: List[str] = []
    business_context: Optional[str] = None

class CompanyCreate(CompanyBase):
    id: Optional[str] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    primary_markets: Optional[List[str]] = None
    business_context: Optional[str] = None

class CompanyProfileResponse(BaseModel):
    id: str
    company_id: str
    business_model: Optional[str] = None
    value_proposition: Optional[str] = None
    pricing_tier: Optional[str] = None
    strategic_priorities: List[str] = []
    key_differentiators: List[str] = []
    risks_and_challenges: List[str] = []
    tech_stack_summary: Optional[str] = None
    generated_by: str = "ai_heuristic"
    updated_at: datetime

    class Config:
        from_attributes = True

class CompanyResponse(CompanyBase):
    id: str
    created_at: datetime
    updated_at: datetime
    profile: Optional[CompanyProfileResponse] = None

    class Config:
        from_attributes = True

class CompanyResearchRequest(BaseModel):
    website: str
    company_name: Optional[str] = None
    industry_hint: Optional[str] = None
