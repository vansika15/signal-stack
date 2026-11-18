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

print("=" * 70)
print("MULTI-COMPANY STATUS & ISOLATION AUDIT")
print("=" * 70)

for comp_id in ["meetuniversity", "stripe", "datadog"]:
    comp = db.query(Company).filter(Company.id == comp_id).first()
    sources = db.query(Source).filter(Source.company_id == comp_id).all()
    comps = db.query(Competitor).filter(Competitor.company_id == comp_id).all()
    items = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == comp_id).all()
    live_items = [i for i in items if i.is_crawled]
    demo_items = [i for i in items if not i.is_crawled]
    latest_report = db.query(MondayReport).filter(MondayReport.company_id == comp_id).order_by(MondayReport.created_at.desc()).first()

    print(f"\n--- COMPANY: {comp.name} ({comp.id}) ---")
    print(f"Domain: {comp.domain} | Industry: {comp.industry}")
    print(f"Sources: {len(sources)} total (Approved: {len([s for s in sources if s.approved_status == 'approved'])}, Healthy: {len([s for s in sources if s.health_status == 'healthy'])})")
    print(f"Competitors: {len(comps)} (Names: {', '.join([c.name for c in comps[:6]])})")
    print(f"Intelligence Items: {len(items)} Total ({len(live_items)} Live Crawled, {len(demo_items)} Seeded Demo)")
    
    if latest_report:
        print(f"Latest Report: {latest_report.id} ({latest_report.report_week})")
        print(f"Report Live Count: {latest_report.live_signals_count}, Demo Count: {latest_report.demo_signals_count}")
        print(f"PDF Export Path: {latest_report.pdf_export_path} (Exists: {os.path.exists(latest_report.pdf_export_path) if latest_report.pdf_export_path else False})")
        
        # Check isolation / cross-contamination
        all_text = " ".join([
            latest_report.section_1_executive_summary or "",
            latest_report.section_2_customer_signals or "",
            latest_report.section_3_competitor_intelligence or "",
            latest_report.section_4_market_intelligence or "",
            latest_report.section_5_internal_intelligence or "",
            latest_report.section_6_opportunities_identified or "",
            latest_report.section_7_risks_and_threats or "",
            latest_report.section_8_recommended_actions or "",
            latest_report.section_9_what_we_should_watch or "",
            latest_report.section_10_source_appendix or ""
        ]).lower()

        if comp_id == "meetuniversity":
            contamination = ("stripe" in all_text) or ("datadog" in all_text)
            print(f"Cross-contamination check (should be False): {contamination}")
        elif comp_id == "stripe":
            contamination = ("meetuniversity" in all_text) or ("student visa" in all_text) or ("datadog" in all_text)
            print(f"Cross-contamination check (should be False): {contamination}")
        elif comp_id == "datadog":
            contamination = ("meetuniversity" in all_text) or ("student visa" in all_text) or ("stripe" in all_text)
            print(f"Cross-contamination check (should be False): {contamination}")

print("\n" + "=" * 70)
db.close()
