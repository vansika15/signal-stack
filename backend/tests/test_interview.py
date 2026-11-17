from app.services.ai_service import AIService

def test_generate_10_interview_questions():
    questions = AIService.generate_10_interview_questions({
        "name": "MeetUniversity",
        "industry": "EdTech",
        "description": "Global university recruitment platform",
        "value_proposition": "Direct student-university matching"
    })
    assert len(questions) == 10
    categories = [q["category"] for q in questions]
    assert "Customer Intelligence" in categories
    assert "Competitor Intelligence" in categories
    assert "Market Intelligence" in categories
    assert "Internal Intelligence" in categories

def test_dynamic_follow_up_generation():
    followup = AIService.generate_follow_up_question(
        question_text="What are the main visa policy bottlenecks affecting your applicants?",
        answer_text="Canada has placed a 35% cap on student visas, forcing us to diversify into Germany.",
        company_context="MeetUniversity (EdTech)"
    )
    assert "follow_up_question" in followup
    assert "strategic_takeaway" in followup
    assert len(followup["follow_up_question"]) > 10
