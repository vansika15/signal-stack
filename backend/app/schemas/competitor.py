from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompetitorBase(BaseModel):
    name: str
    website: Optional[str] = None
    tier: str = "Direct"
    market_focus: Optional[str] = None
    key_strengths: Optional[str] = None
    vulnerabilities: Optional[str] = None
    monitored: bool = True

class CompetitorCreate(CompetitorBase):
    pass

class CompetitorResponse(CompetitorBase):
    id: str
    company_id: str
    discovery_method: str
    created_at: datetime

    class Config:
        from_attributes = True
