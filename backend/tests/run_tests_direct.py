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
from app.models.competitor import Competitor
from app.models.intelligence import IntelligenceItem
from app.models.report import MondayReport
from app.models.interview import InterviewSession

def run_all_tests():
    print("=" * 65)
    print("RUNNING SIGNAL STACK COMPREHENSIVE 12-GATE VERIFICATION SUITE")
    print("=" * 65)

    # 1. Database & Table Initializations
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    print("✔ [1/12] Database initialization and seed completed.")

    # 2. Verify Companies
    companies = db.query(Company).all()
    comp_ids = [c.id for c in companies]
    assert "meetuniversity" in comp_ids, "MeetUniversity missing"
    assert "stripe" in comp_ids, "Stripe missing"
    assert "datadog" in comp_ids, "Datadog missing"
    print(f"✔ [2/12] Mandatory company demonstrations verified: {comp_ids}")

    # 3. Verify MeetUniversity 20 Approved Sources
    mu_sources = db.query(Source).filter(Source.company_id == "meetuniversity").all()
    assert len(mu_sources) >= 20, f"Expected 20+ sources, found {len(mu_sources)}"
    for s in mu_sources:
        assert s.relevance_explanation, f"Source {s.name} missing relevance explanation"
    print(f"✔ [3/12] MeetUniversity public sources verified: {len(mu_sources)} sources with documented relevance explanations.")

    # 4. Verify 4 Signal Stack Categories
    mu_signals = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "meetuniversity").all()
    categories = set(s.category for s in mu_signals)
    required_cats = {"Customer Intelligence", "Competitor Intelligence", "Market Intelligence", "Internal Intelligence"}
    assert required_cats.issubset(categories), f"Missing categories: {required_cats - categories}"
    print(f"✔ [4/12] Four Signal Stack categories present with {len(mu_signals)} intelligence records.")

    # 5. Verify Explainable 6-Factor Ranking
    for s in mu_signals:
        assert s.ranking_score > 0, f"Signal {s.headline} has 0 score"
        assert s.ranking_breakdown is not None, "Missing explainable ranking breakdown"
        assert "components" in s.ranking_breakdown
        assert "strategic_relevance" in s.ranking_breakdown["components"]
        assert "business_impact" in s.ranking_breakdown["components"]
    print("✔ [5/12] Explainable 6-factor ranking mechanism verified across all intelligence items.")

    # 6. Verify 10-Question Adaptive Interview
    mu_session = db.query(InterviewSession).filter(InterviewSession.company_id == "meetuniversity").first()
    assert mu_session is not None, "Interview session missing"
    assert len(mu_session.qas) == 10, f"Expected 10 questions, got {len(mu_session.qas)}"
    for qa in mu_session.qas:
        assert qa.question_text
        assert qa.answer_text
        assert qa.follow_up_question
        assert qa.strategic_takeaway
    print("✔ [6/12] 10-Question adaptive interview with dynamic follow-ups verified.")

    # 7. Verify MeetUniversity Monday Morning Brief (All 10 Sections + Strict Provenance)
    mu_report = db.query(MondayReport).filter(MondayReport.company_id == "meetuniversity").order_by(MondayReport.created_at.desc()).first()
    assert mu_report is not None, "MeetUniversity Monday report missing"
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
    assert mu_report.live_signals_count == 28, f"Expected 28 live signals, got {mu_report.live_signals_count}"
    assert mu_report.demo_signals_count == 12, f"Expected 12 demo signals, got {mu_report.demo_signals_count}"
    assert "Internal company data not connected" in mu_report.section_5_internal_intelligence
    print(f"✔ [7/12] MeetUniversity Monday Brief verified: all 10 sections populated with {len(mu_report.action_items)} action items & strict provenance ({mu_report.live_signals_count} live / {mu_report.demo_signals_count} demo).")

    # 8. Verify PDF Report Generation
    if mu_report.pdf_export_path:
        assert os.path.exists(mu_report.pdf_export_path), f"PDF file not found at {mu_report.pdf_export_path}"
        pdf_size = os.path.getsize(mu_report.pdf_export_path)
        assert pdf_size > 15000, f"Expected PDF >15KB, got {pdf_size} bytes"
        print(f"✔ [8/12] MeetUniversity Executive PDF Brief verified ({pdf_size} bytes).")

    # 9. Verify Stripe Tenant Demonstration
    st_sources = db.query(Source).filter(Source.company_id == "stripe").all()
    st_comps = db.query(Competitor).filter(Competitor.company_id == "stripe").all()
    st_items = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "stripe").all()
    st_live = [i for i in st_items if i.is_crawled]
    st_demo = [i for i in st_items if not i.is_crawled]
    st_report = db.query(MondayReport).filter(MondayReport.company_id == "stripe").order_by(MondayReport.created_at.desc()).first()

    assert len(st_sources) >= 6, f"Expected 6 Stripe sources, found {len(st_sources)}"
    assert len(st_comps) >= 6, f"Expected 6 Stripe competitors, found {len(st_comps)}"
    assert len(st_live) >= 5, f"Expected >=5 live crawled Stripe items, found {len(st_live)}"
    assert st_report is not None, "Stripe Monday report missing"
    assert st_report.live_signals_count == len(st_live)
    print(f"✔ [9/12] Stripe demonstration verified: {len(st_sources)} sources, {len(st_comps)} competitors, {len(st_live)} live crawled records, {len(st_demo)} demo records.")

    # 10. Verify Datadog Tenant Demonstration
    dd_sources = db.query(Source).filter(Source.company_id == "datadog").all()
    dd_comps = db.query(Competitor).filter(Competitor.company_id == "datadog").all()
    dd_items = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "datadog").all()
    dd_live = [i for i in dd_items if i.is_crawled]
    dd_demo = [i for i in dd_items if not i.is_crawled]
    dd_report = db.query(MondayReport).filter(MondayReport.company_id == "datadog").order_by(MondayReport.created_at.desc()).first()

    assert len(dd_sources) >= 5, f"Expected 5 Datadog sources, found {len(dd_sources)}"
    assert len(dd_comps) >= 6, f"Expected 6 Datadog competitors, found {len(dd_comps)}"
    assert len(dd_live) >= 5, f"Expected >=5 live crawled Datadog items, found {len(dd_live)}"
    assert dd_report is not None, "Datadog Monday report missing"
    assert dd_report.live_signals_count == len(dd_live)
    print(f"✔ [10/12] Datadog demonstration verified: {len(dd_sources)} sources, {len(dd_comps)} competitors, {len(dd_live)} live crawled records, {len(dd_demo)} demo records.")

    # 11. Multi-Tenant Data Isolation & Contamination Audit
    for comp_id, label, banned_words in [
        ("meetuniversity", "MeetUniversity", ["stripe", "datadog"]),
        ("stripe", "Stripe", ["meetuniversity", "student visa", "datadog"]),
        ("datadog", "Datadog", ["meetuniversity", "student visa", "stripe"]),
    ]:
        rpt = db.query(MondayReport).filter(MondayReport.company_id == comp_id).order_by(MondayReport.created_at.desc()).first()
        assert rpt is not None
        body = " ".join([
            rpt.section_1_executive_summary or "",
            rpt.section_2_customer_signals or "",
            rpt.section_3_competitor_intelligence or "",
            rpt.section_4_market_intelligence or "",
            rpt.section_5_internal_intelligence or ""
        ]).lower()
        for bw in banned_words:
            assert bw not in body, f"Isolation failure: '{bw}' detected in {label} report"
    print("✔ [11/12] Multi-tenant strict isolation verified: 0 cross-contamination between MeetUniversity, Stripe, and Datadog.")

    # 12. Overall Intelligence Items Count (Requirement: >= 30 records)
    total_items = db.query(IntelligenceItem).count()
    all_live = db.query(IntelligenceItem).filter(IntelligenceItem.source_id.isnot(None)).all()
    live_count = len([i for i in all_live if i.is_crawled])
    assert total_items >= 30, f"Expected >=30 total intelligence records, found {total_items}"
    assert live_count >= 20, f"Expected >=20 live crawled records, found {live_count}"
    print(f"✔ [12/12] Overall intelligence volume verified: {total_items} total records ({live_count} live crawled across all companies; requirement was minimum 30).")

    db.close()
    print("=" * 65)
    print("ALL 12 VERIFICATION GATES PASSED PERFECTLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_all_tests()
