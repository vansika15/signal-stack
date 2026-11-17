import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    source_type = Column(String, nullable=False) # "Competitor Website", "Industry News", "Regulatory/Govt", "Community/Forums", "Job Board", "Review Platform"
    relevance_explanation = Column(Text, nullable=False)
    approved_status = Column(String, default="approved") # "approved", "pending", "rejected"
    health_status = Column(String, default="healthy") # "healthy", "slow", "unreachable", "rate_limited"
    last_crawled_at = Column(DateTime, nullable=True)
    last_status_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    crawl_frequency_hours = Column(Integer, default=24)
    content_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    company = relationship("Company", back_populates="sources")
    crawl_records = relationship("CrawlHistory", back_populates="source", cascade="all, delete-orphan")
    intelligence_items = relationship("IntelligenceItem", back_populates="source")
