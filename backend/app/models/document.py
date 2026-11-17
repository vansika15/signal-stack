import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class InternalDocument(Base):
    __tablename__ = "internal_documents"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    doc_type = Column(String, nullable=False) # "Sales Signals", "Customer Feedback", "Operational Notes", "Executive Memo", "Product Telemetry"
    content = Column(Text, nullable=False)
    extracted_signals_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    company = relationship("Company", back_populates="documents")
