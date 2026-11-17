import time
import datetime
import logging
from typing import Dict, Any, List
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..config import settings
from ..models.company import Company
from ..models.job_log import ScheduledJobLog
from .report_service import ReportService
from .crawler_service import CrawlerService

logger = logging.getLogger(__name__)

class SchedulerService:
    """
    Autonomous Background Automation & Execution Engine:
    - Weekly Monday Morning Intelligence Brief Generator
    - Monthly Source-Health & Availability Audit
    - Periodic Background Crawler Sweeps
    - Execution History & Failed-Job Logging
    - Dynamic Configuration (Timezone, Frequency)
    """

    scheduler: BackgroundScheduler = None

    @classmethod
    def init_scheduler(cls):
        if cls.scheduler is not None and cls.scheduler.running:
            return

        cls.scheduler = BackgroundScheduler(timezone=settings.SCHEDULER_TIMEZONE, daemon=True)

        # 1. Weekly Monday Brief (Every Monday at 08:00 UTC)
        cls.scheduler.add_job(
            cls.run_weekly_brief_job,
            CronTrigger(day_of_week=settings.WEEKLY_REPORT_CRON_DAY, hour=settings.WEEKLY_REPORT_CRON_HOUR, minute=settings.WEEKLY_REPORT_CRON_MINUTE),
            id="weekly_monday_brief",
            name="Weekly Monday Morning Intelligence Brief",
            replace_existing=True
        )

        # 2. Monthly Source-Health Audit (1st of every month at 00:00)
        cls.scheduler.add_job(
            cls.run_monthly_audit_job,
            CronTrigger(day=settings.MONTHLY_AUDIT_DAY, hour=0, minute=0),
            id="monthly_source_audit",
            name="Monthly Source-Health & Availability Audit",
            replace_existing=True
        )

        # 3. Crawler Sweep (Runs every CRAWL_INTERVAL_HOURS)
        cls.scheduler.add_job(
            cls.run_crawler_sweep_job,
            IntervalTrigger(hours=settings.CRAWL_INTERVAL_HOURS),
            id="crawler_sweep",
            name="Periodic Background Crawler Sweep",
            replace_existing=True
        )

        if settings.SCHEDULER_ENABLED:
            cls.scheduler.start()
            logger.info("APScheduler background scheduler started.")

    @classmethod
    def run_weekly_brief_job(cls) -> Dict[str, Any]:
        """Generates Monday briefs for all active companies and logs job history"""
        db = SessionLocal()
        start_time = time.time()
        started_at = datetime.datetime.utcnow()
        status = "success"
        err_msg = None
        count = 0
        
        job_log = ScheduledJobLog(
            id=f"job_{int(time.time()*1000)}_brief",
            job_name="Weekly Monday Morning Intelligence Brief",
            job_type="weekly_brief",
            status="running",
            started_at=started_at
        )
        db.add(job_log)
        db.commit()

        try:
            companies = db.query(Company).all()
            for comp in companies:
                ReportService.generate_brief(db, comp.id)
                count += 1
            summary = f"Successfully generated briefs for {count} companies."
        except Exception as e:
            status = "failed"
            err_msg = str(e)
            summary = f"Job encountered failure: {err_msg}"
            logger.error(f"Weekly brief job failed: {e}")

        finished_at = datetime.datetime.utcnow()
        duration_ms = int((time.time() - start_time) * 1000)

        job_log.status = status
        job_log.finished_at = finished_at
        job_log.duration_ms = duration_ms
        job_log.items_processed = count
        job_log.summary = summary
        job_log.error_message = err_msg
        db.commit()
        db.close()

        return {
            "status": status,
            "items_processed": count,
            "duration_ms": duration_ms,
            "summary": summary
        }

    @classmethod
    def run_monthly_audit_job(cls) -> Dict[str, Any]:
        """Runs monthly source-health audit across all monitored sources"""
        db = SessionLocal()
        start_time = time.time()
        started_at = datetime.datetime.utcnow()
        status = "success"
        err_msg = None
        count = 0

        job_log = ScheduledJobLog(
            id=f"job_{int(time.time()*1000)}_audit",
            job_name="Monthly Source-Health & Availability Audit",
            job_type="monthly_audit",
            status="running",
            started_at=started_at
        )
        db.add(job_log)
        db.commit()

        try:
            audit_results = CrawlerService.audit_sources_health(db)
            count = len(audit_results)
            healthy_count = len([r for r in audit_results if r["health_status"] == "healthy"])
            summary = f"Audited {count} sources: {healthy_count} healthy, {count - healthy_count} degraded/unreachable."
        except Exception as e:
            status = "failed"
            err_msg = str(e)
            summary = f"Source audit failed: {err_msg}"
            logger.error(f"Audit job failed: {e}")

        finished_at = datetime.datetime.utcnow()
        duration_ms = int((time.time() - start_time) * 1000)

        job_log.status = status
        job_log.finished_at = finished_at
        job_log.duration_ms = duration_ms
        job_log.items_processed = count
        job_log.summary = summary
        job_log.error_message = err_msg
        db.commit()
        db.close()

        return {
            "status": status,
            "items_processed": count,
            "duration_ms": duration_ms,
            "summary": summary
        }

    @classmethod
    def run_crawler_sweep_job(cls) -> Dict[str, Any]:
        """Performs scheduled background crawl across approved sources"""
        db = SessionLocal()
        start_time = time.time()
        started_at = datetime.datetime.utcnow()
        status = "success"
        err_msg = None
        count = 0

        job_log = ScheduledJobLog(
            id=f"job_{int(time.time()*1000)}_crawl",
            job_name="Periodic Background Crawler Sweep",
            job_type="crawler_sweep",
            status="running",
            started_at=started_at
        )
        db.add(job_log)
        db.commit()

        try:
            from ..models.source import Source
            sources = db.query(Source).filter(Source.approved_status == "approved").limit(10).all()
            for src in sources:
                CrawlerService.crawl_source(db, src)
                count += 1
            summary = f"Crawl sweep completed across {count} sources."
        except Exception as e:
            status = "failed"
            err_msg = str(e)
            summary = f"Crawl sweep error: {err_msg}"
            logger.error(f"Crawler sweep job failed: {e}")

        finished_at = datetime.datetime.utcnow()
        duration_ms = int((time.time() - start_time) * 1000)

        job_log.status = status
        job_log.finished_at = finished_at
        job_log.duration_ms = duration_ms
        job_log.items_processed = count
        job_log.summary = summary
        job_log.error_message = err_msg
        db.commit()
        db.close()

        return {
            "status": status,
            "items_processed": count,
            "duration_ms": duration_ms,
            "summary": summary
        }
