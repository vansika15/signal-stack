from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InternalDocumentCreate(BaseModel):
    title: str
    doc_type: str # "Sales Signals", "Customer Feedback", "Operational Notes", "Executive Memo", "Product Telemetry"
    content: str

class InternalDocumentResponse(BaseModel):
    id: str
    company_id: str
    title: str
    doc_type: str
    content: str
    extracted_signals_count: int
    created_at: datetime

    class Config:
        from_attributes = True
