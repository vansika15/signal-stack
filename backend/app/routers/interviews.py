from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime
import time

from ..database import get_db
from ..models.company import Company
from ..models.interview import InterviewSession, InterviewQA
from ..schemas.interview import (
    InterviewSessionResponse, InterviewQAResponse, AnswerSubmission, FollowUpAnswerSubmission
)
from ..services.ai_service import AIService

router = APIRouter(prefix="/api/interviews", tags=["Adaptive Interview"])

@router.get("/{company_id}/session", response_model=InterviewSessionResponse)
def get_or_create_session(company_id: str, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    session = db.query(InterviewSession).filter(
        InterviewSession.company_id == company_id
    ).order_by(InterviewSession.created_at.desc()).first()

    if not session:
        session = start_new_interview(company_id, db)
    return session

@router.post("/{company_id}/start", response_model=InterviewSessionResponse)
def start_new_interview(company_id: str, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    # Generate 10 adaptive questions
    questions = AIService.generate_10_interview_questions({
        "name": comp.name,
        "industry": comp.industry,
        "description": comp.description,
        "value_proposition": comp.profile.value_proposition if comp.profile else ""
    })

    session_id = f"session_{int(time.time())}_{company_id[:4]}"
    session = InterviewSession(
        id=session_id,
        company_id=company_id,
        status="in_progress",
        total_questions=len(questions),
        current_question_index=0,
        created_at=datetime.datetime.utcnow()
    )
    db.add(session)

    for q in questions:
        qa = InterviewQA(
            id=f"qa_{int(time.time()*1000)}_{q['question_number']}",
            session_id=session_id,
            question_number=q["question_number"],
            category=q["category"],
            question_text=q["question_text"],
            context_hint=q.get("context_hint"),
            created_at=datetime.datetime.utcnow()
        )
        db.add(qa)

    db.commit()
    db.refresh(session)
    return session

@router.post("/{session_id}/answer/{qa_id}", response_model=InterviewQAResponse)
def submit_answer(session_id: str, qa_id: str, submission: AnswerSubmission, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    qa = db.query(InterviewQA).filter(InterviewQA.id == qa_id, InterviewQA.session_id == session_id).first()
    if not qa:
        raise HTTPException(status_code=404, detail="Question not found")

    qa.answer_text = submission.answer_text
    qa.is_answered = True
    qa.answered_at = datetime.datetime.utcnow()

    # Generate adaptive follow-up and strategic takeaway
    comp = db.query(Company).filter(Company.id == session.company_id).first()
    followup_res = AIService.generate_follow_up_question(
        qa.question_text,
        submission.answer_text,
        company_context=f"{comp.name} ({comp.industry})" if comp else "Enterprise"
    )
    qa.follow_up_question = followup_res.get("follow_up_question")
    qa.strategic_takeaway = followup_res.get("strategic_takeaway")

    # Update session progress
    answered_count = db.query(InterviewQA).filter(
        InterviewQA.session_id == session_id,
        InterviewQA.is_answered == True
    ).count() + 1
    session.current_question_index = min(session.total_questions, answered_count)

    if answered_count >= session.total_questions:
        session.status = "completed"
        session.completed_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(qa)
    return qa

@router.post("/{session_id}/followup/{qa_id}", response_model=InterviewQAResponse)
def submit_follow_up_answer(session_id: str, qa_id: str, submission: FollowUpAnswerSubmission, db: Session = Depends(get_db)):
    qa = db.query(InterviewQA).filter(InterviewQA.id == qa_id, InterviewQA.session_id == session_id).first()
    if not qa:
        raise HTTPException(status_code=404, detail="Question not found")

    qa.follow_up_answer = submission.follow_up_answer
    db.commit()
    db.refresh(qa)
    return qa
