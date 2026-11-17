from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ActionItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str = "Strategic"
    priority: str = "High"
    status: str = "todo"
    owner: Optional[str] = None
    due_date: Optional[str] = None

class ActionItemCreate(ActionItemBase):
    report_id: Optional[str] = None

class ActionItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None # "todo", "in_progress", "completed"
    owner: Optional[str] = None
    due_date: Optional[str] = None

class ActionItemResponse(ActionItemBase):
    id: str
    report_id: Optional[str] = None
    company_id: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MondayReportResponse(BaseModel):
    id: str
    company_id: str
    report_week: str
    title: str
    section_1_executive_summary: str
    section_2_customer_signals: str
    section_3_competitor_intelligence: str
    section_4_market_intelligence: str
    section_5_internal_intelligence: str
    section_6_opportunities_identified: str
    section_7_risks_and_threats: str
    section_8_recommended_actions: str
    section_9_what_we_should_watch: str
    section_10_source_appendix: str
    included_signals_ids: List[str] = []
    pdf_export_path: Optional[str] = None
    created_at: datetime
    action_items: List[ActionItemResponse] = []
    live_signals_count: Optional[int] = 0
    demo_signals_count: Optional[int] = 0
    internal_data_connected: Optional[bool] = False

    class Config:
        from_attributes = True
