import sys
import os
import logging

logging.basicConfig(level=logging.INFO)

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import SessionLocal
from app.models.source import Source
from app.models.intelligence import IntelligenceItem
from app.models.crawl_history import CrawlHistory
from app.services.crawler_service import CrawlerService
from app.services.report_service import ReportService

def main():
    db = SessionLocal()
    try:
        sources = db.query(Source).filter(
            Source.company_id == "datadog",
            Source.approved_status == "approved"
        ).all()
        print(f"Starting crawl for {len(sources)} Datadog sources...")

        for s in sources:
            print(f"\n--- Crawling: {s.name} ({s.url}) ---")
            res = CrawlerService.crawl_source(db, s)
            print(f"Result: status={res.get('status')}, status_code={res.get('status_code')}, items_extracted={res.get('items_extracted')}, error={res.get('error')}")

        db.commit()

        # Count live crawled vs seeded demo items
        items = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "datadog").all()
        live = [i for i in items if i.is_crawled]
        demo = [i for i in items if not i.is_crawled]
        print(f"\nDatadog Intelligence Summary: Total={len(items)}, Live Crawled={len(live)}, Seeded Demo={len(demo)}")
        for l in live:
            print(f"  [LIVE] [{l.category}] {l.headline} | url={l.original_url}")

        # Regenerate Monday Report
        print("\nRegenerating Datadog Monday Brief...")
        report = ReportService.generate_brief(db, "datadog")
        print(f"Generated brief: ID={report.id}, Week={report.report_week}, Title={report.title}")
        print(f"Brief Live Signals: {report.live_signals_count if hasattr(report, 'live_signals_count') else 'N/A'}")
        print(f"Brief Demo Signals: {report.demo_signals_count if hasattr(report, 'demo_signals_count') else 'N/A'}")

        # Generate PDF export
        print("\nExporting PDF for Datadog brief...")
        pdf_path = ReportService.export_pdf(report.id, db)
        print(f"PDF exported to: {pdf_path}")

    finally:
        db.close()

if __name__ == "__main__":
    main()
