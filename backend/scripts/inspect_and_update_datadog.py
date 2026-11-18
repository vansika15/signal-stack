import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import SessionLocal
from app.models.company import Company
from app.models.source import Source
from app.models.competitor import Competitor
from app.models.intelligence import IntelligenceItem
from app.models.report import MondayReport

db = SessionLocal()

for comp_id in ["meetuniversity", "stripe", "datadog"]:
    comp = db.query(Company).filter(Company.id == comp_id).first()
    if not comp:
        print(f"Company {comp_id} not found!")
        continue
    print(f"\n=================== COMPANY: {comp.name} ({comp.id}) ===================")
    sources = db.query(Source).filter(Source.company_id == comp_id).all()
    print(f"Sources ({len(sources)}):")
    for s in sources:
        print(f"  [{s.id}] {s.name} | approved={s.approved_status} | health={s.health_status} | url={s.url}")
    
    competitors = db.query(Competitor).filter(Competitor.company_id == comp_id).all()
    print(f"Competitors ({len(competitors)}):")
    for c in competitors:
        print(f"  [{c.id}] {c.name} ({c.tier}) - {c.website}")

    items = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == comp_id).all()
    live_items = [i for i in items if i.is_crawled]
    demo_items = [i for i in items if not i.is_crawled]
    print(f"Intelligence Items ({len(items)}): {len(live_items)} Live Crawled, {len(demo_items)} Seeded Demo")
    for i in items:
        status_lbl = "LIVE CRAWLED" if i.is_crawled else "SEEDED DEMO"
        print(f"  [{status_lbl}] [{i.id}] {i.category} | {i.headline[:60]}... | source={i.source_id}")

    reports = db.query(MondayReport).filter(MondayReport.company_id == comp_id).all()
    print(f"Reports ({len(reports)}):")
    for r in reports:
        print(f"  [{r.id}] {r.report_week} - {r.title} (created: {r.created_at})")

db.close()
