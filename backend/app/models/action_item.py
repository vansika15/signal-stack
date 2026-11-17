import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(String, primary_key=True, index=True)
    report_id = Column(String, ForeignKey("monday_reports.id", ondelete="CASCADE"), nullable=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, default="Strategic") # "Customer", "Competitor", "Market", "Internal", "Strategic"
    priority = Column(String, default="High") # "Critical", "High", "Medium", "Low"
    status = Column(String, default="todo") # "todo", "in_progress", "completed"
    owner = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    company = relationship("Company", back_populates="action_items")
    report = relationship("MondayReport", back_populates="action_items")
