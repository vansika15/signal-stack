import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class MondayReport(Base):
    __tablename__ = "monday_reports"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    report_week = Column(String, nullable=False) # e.g. "Week 47, 2026"
    title = Column(String, nullable=False)
    
    # 10 Required Sections
    section_1_executive_summary = Column(Text, nullable=False)
    section_2_customer_signals = Column(Text, nullable=False)
    section_3_competitor_intelligence = Column(Text, nullable=False)
    section_4_market_intelligence = Column(Text, nullable=False)
    section_5_internal_intelligence = Column(Text, nullable=False)
    section_6_opportunities_identified = Column(Text, nullable=False)
    section_7_risks_and_threats = Column(Text, nullable=False)
    section_8_recommended_actions = Column(Text, nullable=False)
    section_9_what_we_should_watch = Column(Text, nullable=False)
    section_10_source_appendix = Column(Text, nullable=False)

    included_signals_ids = Column(JSON, default=list)
    pdf_export_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    company = relationship("Company", back_populates="reports")
    action_items = relationship("ActionItem", back_populates="report", cascade="all, delete-orphan")
