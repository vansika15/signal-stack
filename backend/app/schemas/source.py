from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SourceBase(BaseModel):
    name: str
    url: str
    source_type: str
    relevance_explanation: str
    approved_status: str = "approved"

class SourceCreate(SourceBase):
    pass

class SourceStatusUpdate(BaseModel):
    approved_status: str # "approved", "rejected", "pending"

class SourceResponse(SourceBase):
    id: str
    company_id: str
    health_status: str
    last_crawled_at: Optional[datetime] = None
    last_status_code: Optional[int] = None
    error_message: Optional[str] = None
    crawl_frequency_hours: int
    content_hash: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SourceHealthAuditItem(BaseModel):
    source_id: str
    source_name: str
    url: str
    status_code: Optional[int]
    health_status: str
    response_time_ms: int
    error: Optional[str] = None
