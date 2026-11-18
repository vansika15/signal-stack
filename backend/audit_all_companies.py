import json
from app.database import SessionLocal
from app.models.company import Company, CompanyProfile
from app.models.source import Source
from app.models.competitor import Competitor
from app.models.intelligence import IntelligenceItem
from app.models.interview import InterviewSession, InterviewQA
from app.models.report import MondayReport
from app.models.crawl_history import CrawlHistory

db = SessionLocal()

print("=" * 80)
print("COMPREHENSIVE MULTI-COMPANY DATABASE AUDIT")
print("=" * 80)

companies = db.query(Company).all()
print(f"Total Companies: {len(companies)}\n")

for c in companies:
    prof = db.query(CompanyProfile).filter(CompanyProfile.company_id == c.id).first()
    sources = db.query(Source).filter(Source.company_id == c.id).all()
    approved_sources = [s for s in sources if s.approved_status == "approved"]
    healthy_sources = [s for s in sources if s.health_status == "healthy"]
    comps = db.query(Competitor).filter(Competitor.company_id == c.id).all()
    items = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == c.id).all()
    live_items = [i for i in items if i.is_crawled]
    demo_items = [i for i in items if not i.is_crawled]
    interviews = db.query(InterviewSession).filter(InterviewSession.company_id == c.id).all()
    reports = db.query(MondayReport).filter(MondayReport.company_id == c.id).all()
    crawls = db.query(CrawlHistory).filter(CrawlHistory.company_id == c.id).all()

    print(f"Company: {c.name} ({c.id})")
    print(f"  Industry: {c.industry}")
    print(f"  Profile present: {prof is not None}")
    if prof:
        print(f"    Business Model: {prof.business_model[:60] if prof.business_model else 'None'}...")
        print(f"    Strategic Priorities: {len(prof.strategic_priorities or [])} items")
        print(f"    Key Differentiators: {len(prof.key_differentiators or [])} items")
        print(f"    Risks & Challenges: {len(prof.risks_and_challenges or [])} items")
    print(f"  Sources: Total={len(sources)}, Approved={len(approved_sources)}, Healthy={len(healthy_sources)}")
    print(f"  Competitors: Total={len(comps)}")
    for comp in comps[:3]:
        print(f"    - {comp.name} ({comp.tier})")
    if len(comps) > 3:
        print(f"    ... and {len(comps) - 3} more")
    print(f"  Intelligence Records: Total={len(items)} (Live Crawled={len(live_items)}, Seeded Demo={len(demo_items)})")
    # Category breakdown
    cats = {}
    for i in items:
        cats[i.category] = cats.get(i.category, 0) + 1
    print(f"    Category Breakdown: {cats}")
    print(f"  Crawl History Records: Total={len(crawls)}")
    print(f"  Interview Sessions: Total={len(interviews)}")
    for iv in interviews:
        qa_cnt = db.query(InterviewQA).filter(InterviewQA.session_id == iv.id, InterviewQA.is_answered == True).count()
        print(f"    Session {iv.id}: Status={iv.status}, Answered={qa_cnt}/{iv.total_questions}")
    print(f"  Monday Reports: Total={len(reports)}")
    for r in reports:
        print(f"    Report {r.id}: Week={r.report_week}, LiveSignals={r.live_signals_count}, DemoSignals={r.demo_signals_count}")
    print("-" * 60)

total_items = db.query(IntelligenceItem).count()
total_live = len([i for i in db.query(IntelligenceItem).all() if i.is_crawled])
total_demo = total_items - total_live
print(f"\nGLOBAL TOTALS:")
print(f"Total Intelligence Items across all companies: {total_items}")
print(f"Total Live Crawled Items: {total_live}")
print(f"Total Seeded Demo Items: {total_demo}")

db.close()
