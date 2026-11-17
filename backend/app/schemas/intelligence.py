from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class RankingFactorBreakdown(BaseModel):
    relevance: float
    impact: float
    urgency: float
    credibility: float
    recency: float
    novelty: float
    explanation: str

class IntelligenceCreate(BaseModel):
    category: str # "Customer Intelligence", "Competitor Intelligence", "Market Intelligence", "Internal Intelligence"
    headline: str
    summary: str
    evidence: str
    original_url: Optional[str] = None
    source_id: Optional[str] = None
    competitor_id: Optional[str] = None
    verification_status: str = "Verified"
    source_reliability: str = "High"
    evidence_strength: str = "High"
    strategic_relevance: str = "High"
    business_impact: str = "High"
    nature: str = "Opportunity" # "Opportunity", "Threat", "Neutral"
    urgency: str = "Short-Term" # "Immediate", "Short-Term", "Medium-Term", "Watchlist"
    recommended_action: str

class IntelligenceResponse(BaseModel):
    id: str
    company_id: str
    source_id: Optional[str] = None
    competitor_id: Optional[str] = None
    category: str
    headline: str
    summary: str
    evidence: str
    original_url: Optional[str] = None
    publication_date: Optional[datetime] = None
    discovery_date: datetime
    verification_status: str
    source_reliability: str
    evidence_strength: str
    strategic_relevance: str
    business_impact: str
    nature: str
    urgency: str
    recommended_action: str
    ranking_score: float
    ranking_breakdown: Optional[Dict[str, Any]] = None
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True
