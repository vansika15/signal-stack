from app.database import SessionLocal
from app.routers import companies, sources, intelligence, reports, scheduler

def test_api_companies_endpoint():
    db = SessionLocal()
    comps = companies.get_companies(db)
    assert len(comps) >= 3
    ids = [c.id for c in comps]
    assert "meetuniversity" in ids
    assert "stripe" in ids
    assert "datadog" in ids
    db.close()

def test_api_meetuniversity_sources():
    db = SessionLocal()
    srcs = sources.get_sources("meetuniversity", db)
    assert len(srcs) >= 20
    for s in srcs:
        assert s.relevance_explanation
    db.close()

def test_api_intelligence_filtering():
    db = SessionLocal()
    # All items
    all_items = intelligence.get_intelligence("meetuniversity", None, None, None, None, None, False, db)
    assert len(all_items) >= 10
    
    # Customer Intelligence filter
    cust_items = intelligence.get_intelligence("meetuniversity", "Customer Intelligence", None, None, None, None, False, db)
    assert len(cust_items) >= 1
    for item in cust_items:
        assert item.category == "Customer Intelligence"
    db.close()

def test_api_monday_brief_structure():
    db = SessionLocal()
    rpts = reports.get_reports_history("meetuniversity", db)
    assert len(rpts) >= 1
    rpt = rpts[0]
    assert rpt.section_1_executive_summary
    assert rpt.section_2_customer_signals
    assert rpt.section_3_competitor_intelligence
    assert rpt.section_4_market_intelligence
    assert rpt.section_5_internal_intelligence
    assert rpt.section_6_opportunities_identified
    assert rpt.section_7_risks_and_threats
    assert rpt.section_8_recommended_actions
    assert rpt.section_9_what_we_should_watch
    assert rpt.section_10_source_appendix
    db.close()

def test_api_scheduler_status():
    status = scheduler.get_scheduler_status()
    assert "enabled" in status
    assert "timezone" in status
    assert "weekly_brief_schedule" in status
