from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InterviewQAResponse(BaseModel):
    id: str
    session_id: str
    question_number: int
    category: str
    question_text: str
    context_hint: Optional[str] = None
    answer_text: Optional[str] = None
    is_answered: bool
    follow_up_question: Optional[str] = None
    follow_up_answer: Optional[str] = None
    strategic_takeaway: Optional[str] = None
    created_at: datetime
    answered_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AnswerSubmission(BaseModel):
    answer_text: str

class FollowUpAnswerSubmission(BaseModel):
    follow_up_answer: str

class InterviewSessionResponse(BaseModel):
    id: str
    company_id: str
    status: str
    total_questions: int
    current_question_index: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    qas: List[InterviewQAResponse] = []

    class Config:
        from_attributes = True
