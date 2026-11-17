import os
import sys
import time
import json
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.database import SessionLocal
from app.models.source import Source
from app.models.crawl_history import CrawlHistory
from app.models.intelligence import IntelligenceItem
from app.services.crawler_service import CrawlerService
from app.services.ranking_service import RankingService

def main():
    db = SessionLocal()
    print("=" * 80)
    print("SIGNAL STACK – ENHANCED CRAWLER & EXTRACTION EVALUATION AUDIT")
    print("=" * 80)

    # 1. Inspect all 20 MeetUniversity Sources
    sources = db.query(Source).filter(Source.company_id == "meetuniversity").order_by(Source.id.asc()).all()
    print(f"\n1. INSPECTING {len(sources)} RECONFIGURED SOURCES FOR MEETUNIVERSITY:\n")
    for i, s in enumerate(sources, 1):
        print(f"[{i:02d}] {s.name:<45} | Type: {s.source_type:<20}")
        print(f"     URL: {s.url}")
        print(f"     Relevance: {s.relevance_explanation[:90]}...")

    # Record baseline records before crawl
    existing_records = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "meetuniversity").all()
    initial_seeded = [r for r in existing_records if not r.is_crawled]
    initial_crawled = [r for r in existing_records if r.is_crawled]
    print(f"\nInitial State: {len(initial_seeded)} Seeded Baseline Records | {len(initial_crawled)} Previously Crawled Records")

    # 2. Run Enhanced Crawler on All 20 Sources
    print("\n" + "=" * 80)
    print("2. EXECUTING LIVE CRAWLER PASS WITH BOILERPLATE REJECTION & SEMANTIC EXTRACTION")
    print("=" * 80 + "\n")

    crawl_results = []
    for idx, s in enumerate(sources, 1):
        print(f"--> [{idx:02d}/{len(sources)}] Crawling: {s.name} ({s.url})...")
        t0 = time.time()
        res = CrawlerService.crawl_source(db, s)
        elapsed = round(time.time() - t0, 2)
        print(f"    Code: {res['status_code']} | Health: {res['health_status']} | Diff: {res['has_changes']} | Extracted: {res['signals_extracted']} ({elapsed}s)")
        crawl_results.append(res)
        time.sleep(0.4) # polite delay between domains

    # 3. Test SHA-256 Deduplication (Second Pass)
    print("\n" + "=" * 80)
    print("3. EXECUTING 2ND PASS TEST FOR SHA-256 CHANGE DETECTION & DEDUPLICATION")
    print("=" * 80 + "\n")

    test_sources = [s for s in sources if s.health_status == "healthy"][:3]
    for s in test_sources:
        print(f"Re-crawling for duplicate check: {s.name}...")
        t0 = time.time()
        res2 = CrawlerService.crawl_source(db, s)
        print(f"    Content Hash: {s.content_hash[:24]}...")
        print(f"    has_changes: {res2['has_changes']} | signals_extracted: {res2['signals_extracted']}")
        if not res2["has_changes"] and res2["signals_extracted"] == 0:
            print("    ✔ SHA-256 match confirmed: Zero duplicate signals created.\n")
        else:
            print("    ⚠ Warning: Duplicate signals or unexpected diff detected.\n")

    # 4. Analyze Extraction Quality & Boilerplate Rejection
    print("=" * 80)
    print("4. INTELLIGENCE EXTRACTION QUALITY & SUBSTANTIVE DEVELOPMENTS")
    print("=" * 80 + "\n")

    current_records = db.query(IntelligenceItem).filter(IntelligenceItem.company_id == "meetuniversity").order_by(IntelligenceItem.created_at.desc()).all()
    crawled_items = [r for r in current_records if r.is_crawled]
    seeded_items = [r for r in current_records if not r.is_crawled]

    print(f"Total Records in Database: {len(current_records)}")
    print(f"  - Seeded Baseline Records (Preserved): {len(seeded_items)}")
    print(f"  - Genuinely Crawled Intelligence Records: {len(crawled_items)}\n")

    print("SAMPLE OF RECENTLY CRAWLED SUBSTANTIVE RECORDS (TOP 6):")
    for idx, item in enumerate(crawled_items[:6], 1):
        print(f"\n--- [CRAWLED ITEM #{idx}] ---")
        print(f"Headline: {item.headline}")
        print(f"Category: {item.category} | Nature: {item.nature} | Urgency: {item.urgency}")
        print(f"Origin URL: {item.original_url}")
        print(f"Publication Date: {item.publication_date}")
        print(f"Summary: {item.summary[:180]}...")
        print(f"Verifiable Evidence: {item.evidence}")
        print(f"Calculated Score: {item.ranking_score}/100")
        print(f"Relevance: {item.strategic_relevance} | Impact: {item.business_impact} | Credibility: {item.source_reliability}")

    # 5. Check Score Distribution
    scores = [r.ranking_score for r in crawled_items]
    if scores:
        print("\n" + "=" * 80)
        print("5. SCORE CALIBRATION & DISTRIBUTION SUMMARY")
        print("=" * 80)
        print(f"Total Crawled Scores Analyzed: {len(scores)}")
        print(f"Min Score: {min(scores)} | Max Score: {max(scores)} | Average: {round(sum(scores)/len(scores), 1)}")
        perfect_100s = [s for s in scores if s == 100.0]
        print(f"Scores at 100.0: {len(perfect_100s)} (Should be strictly rare and justified)")
        print(f"Scores 80.0 - 95.0: {len([s for s in scores if 80.0 <= s < 100.0])}")
        print(f"Scores < 80.0: {len([s for s in scores if s < 80.0])}")

    db.close()
    print("\n" + "=" * 80)
    print("EVALUATION AUDIT COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
