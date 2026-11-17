import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime
from ..database import Base

class ScheduledJobLog(Base):
    __tablename__ = "scheduled_job_logs"

    id = Column(String, primary_key=True, index=True)
    job_name = Column(String, nullable=False) # "weekly_monday_brief", "monthly_source_audit", "crawler_sweep"
    job_type = Column(String, nullable=False)
    status = Column(String, nullable=False) # "success", "failed", "running"
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, default=0)
    items_processed = Column(Integer, default=0)
    summary = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
