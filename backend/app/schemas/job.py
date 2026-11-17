from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScheduledJobLogResponse(BaseModel):
    id: str
    job_name: str
    job_type: str
    status: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    duration_ms: int
    items_processed: int
    summary: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

class SchedulerConfigUpdate(BaseModel):
    timezone: Optional[str] = None
    frequency_hours: Optional[int] = None
    enabled: Optional[bool] = None
