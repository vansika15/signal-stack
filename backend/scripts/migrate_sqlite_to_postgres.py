"""
Signal Stack: SQLite to PostgreSQL Migration Engine
----------------------------------------------------
Transfers all existing seeded companies, verified crawled intelligence items,
crawl history, Monday reports, interview sessions, sources, competitors, and
action items from SQLite (signal_stack.db) to a target PostgreSQL database.

Usage:
    python backend/scripts/migrate_sqlite_to_postgres.py [POSTGRES_URL]

If POSTGRES_URL is omitted, reads from the TARGET_DATABASE_URL or DATABASE_URL environment variable.
"""

import sys
import os
import logging
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("migration")

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import Base
# Import all models to ensure metadata registration
from app.models.company import Company, CompanyProfile
from app.models.interview import InterviewSession, InterviewQA
from app.models.competitor import Competitor
from app.models.source import Source
from app.models.intelligence import IntelligenceItem
from app.models.document import InternalDocument
from app.models.report import MondayReport
from app.models.action_item import ActionItem
from app.models.crawl_history import CrawlHistory
from app.models.job_log import ScheduledJobLog

# Table migration order respecting foreign key constraints
TABLE_ORDER = [
    "companies",
    "company_profiles",
    "interview_sessions",
    "interview_qas",
    "competitors",
    "sources",
    "crawl_history",
    "intelligence_items",
    "internal_documents",
    "monday_reports",
    "action_items",
    "scheduled_job_logs"
]

def migrate(sqlite_path: str, pg_url: str):
    if not os.path.exists(sqlite_path):
        logger.error(f"Source SQLite database not found at: {sqlite_path}")
        sys.exit(1)

    # Normalize postgres URL for SQLAlchemy 2.0 with psycopg2
    if pg_url.startswith("postgres://"):
        pg_url = pg_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif pg_url.startswith("postgresql://") and not pg_url.startswith("postgresql+"):
        pg_url = pg_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    logger.info("=" * 70)
    logger.info("SIGNAL STACK: SQLITE -> POSTGRESQL DATA MIGRATION")
    logger.info("=" * 70)
    logger.info(f"Source: SQLite ({sqlite_path})")
    logger.info(f"Target: PostgreSQL ({pg_url.split('@')[-1] if '@' in pg_url else pg_url})")

    # 1. Connect to SQLite
    sqlite_engine = create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})
    
    # 2. Connect to PostgreSQL
    try:
        pg_engine = create_engine(pg_url)
        with pg_engine.connect() as conn:
            logger.info("✔ Successfully connected to target PostgreSQL database.")
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        logger.error("Verify that your PostgreSQL server is running and reachable.")
        sys.exit(1)

    # 3. Create all tables in PostgreSQL
    logger.info("Creating schema and tables in PostgreSQL if not present...")
    Base.metadata.create_all(bind=pg_engine)
    logger.info("✔ PostgreSQL schema tables verified.")

    # 4. Copy records table-by-table
    sqlite_meta = MetaData()
    sqlite_meta.reflect(bind=sqlite_engine)

    pg_meta = MetaData()
    pg_meta.reflect(bind=pg_engine)

    total_rows = 0
    with sqlite_engine.connect() as sqlite_conn, pg_engine.connect() as pg_conn:
        for table_name in TABLE_ORDER:
            if table_name not in sqlite_meta.tables:
                logger.warning(f"Table {table_name} not found in SQLite source; skipping.")
                continue

            src_table = sqlite_meta.tables[table_name]
            dest_table = pg_meta.tables[table_name]

            # Fetch existing records in target to avoid duplicates
            existing_target_ids = set()
            if "id" in dest_table.c:
                existing_res = pg_conn.execute(select(dest_table.c.id)).fetchall()
                existing_target_ids = {r[0] for r in existing_res}

            # Read source records
            rows = sqlite_conn.execute(select(src_table)).mappings().all()
            if not rows:
                logger.info(f"  [{table_name}] 0 rows in source.")
                continue

            # Filter out already existing rows in destination
            records_to_insert = []
            for row in rows:
                row_dict = dict(row)
                row_id = row_dict.get("id")
                if row_id and row_id in existing_target_ids:
                    continue
                records_to_insert.append(row_dict)

            if records_to_insert:
                pg_conn.execute(dest_table.insert(), records_to_insert)
                pg_conn.commit()
                logger.info(f"  ✔ [{table_name}] Migrated {len(records_to_insert)} records (Skipped {len(rows) - len(records_to_insert)} existing).")
                total_rows += len(records_to_insert)
            else:
                logger.info(f"  ✔ [{table_name}] All {len(rows)} records already present in target.")

    logger.info("=" * 70)
    logger.info(f"MIGRATION COMPLETE: {total_rows} total records migrated into PostgreSQL without loss.")
    logger.info("=" * 70)

if __name__ == "__main__":
    default_sqlite = os.path.join(backend_dir, "signal_stack.db")
    target_url = None

    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = os.environ.get("TARGET_DATABASE_URL") or os.environ.get("DATABASE_URL")

    if not target_url or target_url.startswith("sqlite"):
        print("Usage:")
        print("  python backend/scripts/migrate_sqlite_to_postgres.py postgresql://user:pass@host:5432/dbname")
        print("\nOr set TARGET_DATABASE_URL environment variable.")
        sys.exit(0)

    migrate(default_sqlite, target_url)
