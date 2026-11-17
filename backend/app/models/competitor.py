import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    website = Column(String, nullable=True)
    tier = Column(String, default="Direct") # "Direct", "Indirect", "Emerging"
    market_focus = Column(String, nullable=True)
    key_strengths = Column(Text, nullable=True)
    vulnerabilities = Column(Text, nullable=True)
    monitored = Column(Boolean, default=True)
    discovery_method = Column(String, default="ai_discovered") # "ai_discovered", "manual"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    company = relationship("Company", back_populates="competitors")
