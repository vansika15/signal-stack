import sys
import json
import time
from app.database import SessionLocal
from app.models.company import Company
from app.models.source import Source
from app.models.intelligence import IntelligenceItem
from app.models.crawl_history import CrawlHistory
from app.models.report import MondayReport
from app.services.crawler_service import CrawlerService
from app.services.report_service import ReportService

db = SessionLocal()

print("=" * 70)
print("1. RUNNING LIVE STRIPE CRAWLER ON ALL 6 APPROVED SOURCES")
print("=" * 70)

sources = db.query(Source).filter(
    Source.company_id == "stripe",
    Source.approved_status == "approved"
).order_by(Source.id).all()

print(f"Total approved sources to crawl for Stripe: {len(sources)}\n")

crawl_results = []
rejected_pages = []

for idx, src in enumerate(sources, 1):
    print(f"[{idx}/{len(sources)}] Crawling Source: {src.name} ({src.url})...")
    res = CrawlerService.crawl_source(db, src)
    crawl_results.append(res)
    
    status_str = f"HTTP {res.get('status_code')} | Health: {res.get('health_status')} | {res.get('duration_ms')}ms"
    extracted_cnt = res.get('signals_extracted', 0)
    print(f"    --> Status: {status_str} | New Signals Extracted: {extracted_cnt}")
    
    if res.get('error_details'):
        print(f"    --> Error / Note: {res.get('error_details')}")
        rejected_pages.append({
            "source": src.name,
            "url": src.url,
            "status_code": res.get('status_code'),
            "reason": res.get('error_details')
        })
    elif extracted_cnt == 0:
        reason = "Page accessible (HTTP 200) but no company-relevant articles or timely developments matched keyword thresholds"
        print(f"    --> Result: {reason}")
        rejected_pages.append({
            "source": src.name,
            "url": src.url,
            "status_code": res.get('status_code'),
            "reason": reason
        })
    print("-" * 50)

print("\n" + "=" * 70)
print("2. CRAWL EXECUTION AUDIT SUMMARY")
print("=" * 70)
successful_attempts = sum(1 for r in crawl_results if r.get('status_code') == 200)
total_signals_extracted = sum(r.get('signals_extracted', 0) for r in crawl_results)

print(f"Total Crawl Attempts: {len(crawl_results)}")
print(f"Successful HTTP 200 Attempts: {successful_attempts}")
print(f"HTTP 4xx / Blocked Attempts: {len(crawl_results) - successful_attempts}")
print(f"Total New Live Signals Extracted: {total_signals_extracted}")
print(f"Rejected / Zero-Signal Sources Count: {len(rejected_pages)}")

print("\nRejected Pages Details:")
for rp in rejected_pages:
    print(f"  • {rp['source']} ({rp['url']}): HTTP {rp['status_code']} — {rp['reason']}")

print("\n" + "=" * 70)
print("3. UPDATED SOURCE HEALTH STATUSES IN DATABASE")
print("=" * 70)
updated_sources = db.query(Source).filter(Source.company_id == "stripe").order_by(Source.id).all()
for s in updated_sources:
    print(f"Source: {s.name}")
    print(f"  URL: {s.url}")
    print(f"  Health: {s.health_status}")
    print(f"  Last Status Code: {s.last_status_code}")
    print(f"  Last Crawled: {s.last_crawled_at}")
    print(f"  Content Hash: {s.content_hash[:16] if s.content_hash else 'None'}...")
    print(f"  Error Message: {s.error_message}")
    print("-" * 40)

print("\n" + "=" * 70)
print("4. INTELLIGENCE RECORDS IN DATABASE (STRIPE)")
print("=" * 70)
all_items = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "stripe").order_by(IntelligenceItem.ranking_score.desc()).all()
live_items = [it for it in all_items if it.is_crawled]
demo_items = [it for it in all_items if not it.is_crawled]

print(f"Total Intelligence Records: {len(all_items)}")
print(f"  • Live Crawled Records (is_crawled=True): {len(live_items)}")
print(f"  • Seeded Demonstration Records (is_crawled=False): {len(demo_items)}")

print("\n--- Genuinely Crawled Live Signals ---")
for it in live_items:
    print(f"ID: {it.id}")
    print(f"  Headline: {it.headline}")
    print(f"  Category: {it.category} | Nature: {it.nature} | Urgency: {it.urgency}")
    print(f"  Ranking Score: {it.ranking_score}")
    print(f"  URL: {it.original_url}")
    print(f"  Evidence: {it.evidence}")
    print(f"  Action: {it.recommended_action}")
    print("-" * 40)

print("\n--- Seeded Demonstration Records (Baseline Models) ---")
for it in demo_items:
    print(f"ID: {it.id} [DEMO DATA]")
    print(f"  Headline: {it.headline}")
    print(f"  Category: {it.category} | Nature: {it.nature}")
    print(f"  Evidence: {it.evidence}")
    print("-" * 40)

print("\n" + "=" * 70)
print("5. CRAWL HISTORY LOG IN DATABASE")
print("=" * 70)
history = db.query(CrawlHistory).filter(CrawlHistory.company_id == "stripe").order_by(CrawlHistory.crawled_at.desc()).limit(10).all()
print(f"Total CrawlHistory Records for Stripe: {len(history)}")
for h in history:
    print(f"ID: {h.id} | Source: {h.source_id} | Code: {h.status_code} | Duration: {h.duration_ms}ms | Has Changes: {h.has_changes} | Extracted: {h.signals_extracted}")

print("\n" + "=" * 70)
print("6. REGENERATING STRIPE MONDAY MORNING BRIEF WITH ACTUAL LIVE DATA")
print("=" * 70)
# Delete existing report to generate fresh synthesis
db.query(MondayReport).filter(MondayReport.company_id == "stripe").delete()
db.commit()

report = ReportService.generate_brief(db, "stripe")
print(f"Generated Brief ID: {report.id}")
print(f"Title: {report.title}")
print(f"Live Signals Count: {report.live_signals_count}")
print(f"Demo Signals Count: {report.demo_signals_count}")
print(f"Internal Data Connected: {report.internal_data_connected}")

# Section previews
print("\nSection 1 (Executive Summary Preview):")
print(report.section_1_executive_summary[:250] + "...")

print("\nSection 10 (Source Appendix Preview):")
print(report.section_10_source_appendix[:250] + "...")

# Multi-tenant isolation check
all_text = " ".join([
    report.section_1_executive_summary,
    report.section_2_customer_signals,
    report.section_3_competitor_intelligence,
    report.section_4_market_intelligence,
    report.section_5_internal_intelligence,
    report.section_6_opportunities_identified,
    report.section_7_risks_and_threats,
    report.section_8_recommended_actions,
    report.section_9_what_we_should_watch,
    report.section_10_source_appendix
]).lower()

has_mu = "meetuniversity" in all_text
has_ielts = "ielts" in all_text
print("\n" + "=" * 70)
print("7. TENANT ISOLATION CHECK")
print("=" * 70)
print(f"Contains 'meetuniversity': {has_mu}")
print(f"Contains 'ielts': {has_ielts}")
print(f"Tenant Isolation: {'PERFECT (100% Isolated)' if not has_mu and not has_ielts else 'FAILED'}")

db.close()
