import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class CrawlHistory(Base):
    __tablename__ = "crawl_history"

    id = Column(String, primary_key=True, index=True)
    source_id = Column(String, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(String, nullable=False)
    crawled_at = Column(DateTime, default=datetime.datetime.utcnow)
    status_code = Column(Integer, nullable=True)
    duration_ms = Column(Integer, default=0)
    content_hash = Column(String, nullable=True)
    has_changes = Column(Boolean, default=False)
    signals_extracted = Column(Integer, default=0)
    response_size_bytes = Column(Integer, default=0)
    error_details = Column(Text, nullable=True)

    source = relationship("Source", back_populates="crawl_records")
