from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database import get_db
from ..models.job_log import ScheduledJobLog
from ..schemas.job import ScheduledJobLogResponse, SchedulerConfigUpdate
from ..services.scheduler_service import SchedulerService
from ..config import settings

router = APIRouter(prefix="/api/scheduler", tags=["Scheduler & Automation"])

@router.get("/status")
def get_scheduler_status():
    running = SchedulerService.scheduler is not None and SchedulerService.scheduler.running
    jobs_info = []
    if running:
        for job in SchedulerService.scheduler.get_jobs():
            jobs_info.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": str(job.next_run_time) if job.next_run_time else None
            })

    return {
        "enabled": settings.SCHEDULER_ENABLED,
        "running": running,
        "timezone": settings.SCHEDULER_TIMEZONE,
        "weekly_brief_schedule": f"Every {settings.WEEKLY_REPORT_CRON_DAY.capitalize()} at {settings.WEEKLY_REPORT_CRON_HOUR:02d}:{settings.WEEKLY_REPORT_CRON_MINUTE:02d} {settings.SCHEDULER_TIMEZONE}",
        "monthly_audit_schedule": f"1st of every month at 00:00 {settings.SCHEDULER_TIMEZONE}",
        "crawl_interval_hours": settings.CRAWL_INTERVAL_HOURS,
        "active_jobs": jobs_info
    }

@router.get("/history", response_model=List[ScheduledJobLogResponse])
def get_job_history(db: Session = Depends(get_db)):
    return db.query(ScheduledJobLog).order_by(ScheduledJobLog.started_at.desc()).limit(30).all()

@router.post("/trigger/{job_name}")
def trigger_job(job_name: str):
    if job_name == "weekly_brief":
        res = SchedulerService.run_weekly_brief_job()
        return {"message": "Weekly brief job triggered successfully", "result": res}
    elif job_name == "monthly_audit":
        res = SchedulerService.run_monthly_audit_job()
        return {"message": "Monthly source audit triggered successfully", "result": res}
    elif job_name == "crawler_sweep":
        res = SchedulerService.run_crawler_sweep_job()
        return {"message": "Crawler sweep triggered successfully", "result": res}
    else:
        raise HTTPException(status_code=400, detail="Invalid job name. Valid names: weekly_brief, monthly_audit, crawler_sweep")

@router.put("/config")
def update_scheduler_config(req: SchedulerConfigUpdate):
    if req.timezone is not None:
        settings.SCHEDULER_TIMEZONE = req.timezone
    if req.frequency_hours is not None:
        settings.CRAWL_INTERVAL_HOURS = req.frequency_hours
    if req.enabled is not None:
        settings.SCHEDULER_ENABLED = req.enabled
    return {"message": "Scheduler configuration updated successfully", "config": req}
