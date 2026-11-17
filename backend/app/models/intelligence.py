import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class IntelligenceItem(Base):
    __tablename__ = "intelligence_items"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    competitor_id = Column(String, ForeignKey("competitors.id", ondelete="SET NULL"), nullable=True)
    
    # Category: Customer, Competitor, Market, Internal
    category = Column(String, nullable=False, index=True)
    
    headline = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    evidence = Column(Text, nullable=False) # Direct factual quote, stats, or excerpt
    original_url = Column(String, nullable=True)
    
    publication_date = Column(DateTime, nullable=True)
    discovery_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    verification_status = Column(String, default="Verified") # "Verified", "Pending Verification", "Unverified"
    source_reliability = Column(String, default="High") # "High", "Medium", "Low"
    evidence_strength = Column(String, default="High") # "High", "Medium", "Low"
    strategic_relevance = Column(String, default="High") # "High", "Medium", "Low"
    business_impact = Column(String, default="High") # "High", "Medium", "Low"
    
    nature = Column(String, default="Opportunity") # "Opportunity", "Threat", "Neutral"
    urgency = Column(String, default="Short-Term") # "Immediate", "Short-Term", "Medium-Term", "Watchlist"
    recommended_action = Column(Text, nullable=False)
    
    # Explainable ranking mechanism
    ranking_score = Column(Float, default=0.0) # 0 to 100
    ranking_breakdown = Column(JSON, default=dict) # breakdown of relevance, impact, urgency, credibility, recency, novelty
    
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    company = relationship("Company", back_populates="intelligence_items")
    source = relationship("Source", back_populates="intelligence_items")
