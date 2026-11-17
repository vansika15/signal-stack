import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, index=True) # e.g. "meetuniversity", "stripe", "datadog"
    name = Column(String, nullable=False)
    website = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    target_audience = Column(String, nullable=True)
    primary_markets = Column(JSON, default=list) # List of market strings
    business_context = Column(Text, nullable=True) # Dynamic context that can change
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    profile = relationship("CompanyProfile", back_populates="company", uselist=False, cascade="all, delete-orphan")
    competitors = relationship("Competitor", back_populates="company", cascade="all, delete-orphan")
    sources = relationship("Source", back_populates="company", cascade="all, delete-orphan")
    intelligence_items = relationship("IntelligenceItem", back_populates="company", cascade="all, delete-orphan")
    interview_sessions = relationship("InterviewSession", back_populates="company", cascade="all, delete-orphan")
    reports = relationship("MondayReport", back_populates="company", cascade="all, delete-orphan")
    documents = relationship("InternalDocument", back_populates="company", cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="company", cascade="all, delete-orphan")

class CompanyProfile(Base):
    __tablename__ = "company_profiles"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, unique=True)
    business_model = Column(Text, nullable=True)
    value_proposition = Column(Text, nullable=True)
    pricing_tier = Column(String, nullable=True)
    strategic_priorities = Column(JSON, default=list)
    key_differentiators = Column(JSON, default=list)
    risks_and_challenges = Column(JSON, default=list)
    tech_stack_summary = Column(Text, nullable=True)
    generated_by = Column(String, default="ai_heuristic") # "gemini" or "heuristic"
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    company = relationship("Company", back_populates="profile")
