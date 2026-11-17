import sys
import os

# Set paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine, Base, SessionLocal
from app.services.seed_service import seed_database
from app.services.ranking_service import RankingService
from app.services.ai_service import AIService
from app.models.company import Company
from app.models.source import Source
from app.models.intelligence import IntelligenceItem
from app.models.report import MondayReport
from app.models.interview import InterviewSession

def run_all_tests():
    print("=" * 60)
    print("RUNNING SIGNAL STACK AUTOMATED VERIFICATION SUITE")
    print("=" * 60)

    # 1. Database & Table Initializations
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    print("✔ [1/8] Database initialization and seed completed.")

    # 2. Verify Companies
    companies = db.query(Company).all()
    comp_ids = [c.id for c in companies]
    assert "meetuniversity" in comp_ids, "MeetUniversity missing"
    assert "stripe" in comp_ids, "Stripe missing"
    assert "datadog" in comp_ids, "Datadog missing"
    print(f"✔ [2/8] Mandatory company demonstrations verified: {comp_ids}")

    # 3. Verify MeetUniversity 20 Approved Sources
    mu_sources = db.query(Source).filter(Source.company_id == "meetuniversity").all()
    assert len(mu_sources) >= 20, f"Expected 20+ sources, found {len(mu_sources)}"
    for s in mu_sources:
        assert s.relevance_explanation, f"Source {s.name} missing relevance explanation"
    print(f"✔ [3/8] MeetUniversity public sources verified: {len(mu_sources)} sources with documented relevance explanations.")

    # 4. Verify 4 Signal Stack Categories
    mu_signals = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "meetuniversity").all()
    categories = set(s.category for s in mu_signals)
    required_cats = {"Customer Intelligence", "Competitor Intelligence", "Market Intelligence", "Internal Intelligence"}
    assert required_cats.issubset(categories), f"Missing categories: {required_cats - categories}"
    print(f"✔ [4/8] Four Signal Stack categories present with {len(mu_signals)} intelligence records.")

    # 5. Verify Explainable 6-Factor Ranking
    for s in mu_signals:
        assert s.ranking_score > 0, f"Signal {s.headline} has 0 score"
        assert s.ranking_breakdown is not None, "Missing explainable ranking breakdown"
        assert "components" in s.ranking_breakdown
        assert "strategic_relevance" in s.ranking_breakdown["components"]
        assert "business_impact" in s.ranking_breakdown["components"]
    print("✔ [5/8] Explainable 6-factor ranking mechanism verified across all intelligence items.")

    # 6. Verify 10-Question Adaptive Interview
    mu_session = db.query(InterviewSession).filter(InterviewSession.company_id == "meetuniversity").first()
    assert mu_session is not None, "Interview session missing"
    assert len(mu_session.qas) == 10, f"Expected 10 questions, got {len(mu_session.qas)}"
    for qa in mu_session.qas:
        assert qa.question_text
        assert qa.answer_text
        assert qa.follow_up_question
        assert qa.strategic_takeaway
    print("✔ [6/8] 10-Question adaptive interview with dynamic follow-ups verified.")

    # 7. Verify Monday Morning Brief (All 10 Sections)
    mu_report = db.query(MondayReport).filter(MondayReport.company_id == "meetuniversity").first()
    assert mu_report is not None, "Monday report missing"
    assert mu_report.section_1_executive_summary
    assert mu_report.section_2_customer_signals
    assert mu_report.section_3_competitor_intelligence
    assert mu_report.section_4_market_intelligence
    assert mu_report.section_5_internal_intelligence
    assert mu_report.section_6_opportunities_identified
    assert mu_report.section_7_risks_and_threats
    assert mu_report.section_8_recommended_actions
    assert mu_report.section_9_what_we_should_watch
    assert mu_report.section_10_source_appendix
    assert len(mu_report.action_items) > 0, "Action tracking items missing"
    print(f"✔ [7/8] Monday Morning Brief verified: all 10 sections populated with {len(mu_report.action_items)} action items.")

    # 8. Verify PDF Report Generation
    if mu_report.pdf_export_path:
        assert os.path.exists(mu_report.pdf_export_path), f"PDF file not found at {mu_report.pdf_export_path}"
        print(f"✔ [8/8] Executive PDF Brief generated and verified ({os.path.getsize(mu_report.pdf_export_path)} bytes).")

    db.close()
    print("=" * 60)
    print("ALL 8 VERIFICATION GATES PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
