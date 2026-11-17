import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="in_progress") # "in_progress", "completed"
    total_questions = Column(Integer, default=10)
    current_question_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    company = relationship("Company", back_populates="interview_sessions")
    qas = relationship("InterviewQA", back_populates="session", cascade="all, delete-orphan", order_by="InterviewQA.question_number")

class InterviewQA(Base):
    __tablename__ = "interview_qas"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    question_number = Column(Integer, nullable=False)
    category = Column(String, nullable=False) # "Customer", "Competitor", "Market", "Internal"
    question_text = Column(Text, nullable=False)
    context_hint = Column(Text, nullable=True)
    answer_text = Column(Text, nullable=True)
    is_answered = Column(Boolean, default=False)
    
    # Adaptive follow-up
    follow_up_question = Column(Text, nullable=True)
    follow_up_answer = Column(Text, nullable=True)
    strategic_takeaway = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    answered_at = Column(DateTime, nullable=True)

    session = relationship("InterviewSession", back_populates="qas")
