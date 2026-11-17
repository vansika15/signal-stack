import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from ..config import settings

router = APIRouter(prefix="/api/settings", tags=["Settings"])

class SettingsUpdate(BaseModel):
    gemini_api_key: Optional[str] = None
    scheduler_timezone: Optional[str] = None
    crawl_interval_hours: Optional[int] = None

@router.get("")
def get_settings():
    api_key_set = bool(settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY"))
    masked_key = ""
    curr_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
    if curr_key and len(curr_key) > 8:
        masked_key = f"{curr_key[:4]}...{curr_key[-4:]}"

    return {
        "app_name": settings.APP_NAME,
        "app_env": settings.APP_ENV,
        "database_url": settings.DATABASE_URL,
        "database_type": "PostgreSQL Compatible SQLite Engine",
        "gemini_api_key_configured": api_key_set,
        "gemini_api_key_masked": masked_key,
        "ai_active_engine": "Gemini 1.5 Flash (Live API)" if api_key_set else "Domain Strategic Semantic Inference Engine (Airgapped/Fallback)",
        "scheduler_enabled": settings.SCHEDULER_ENABLED,
        "scheduler_timezone": settings.SCHEDULER_TIMEZONE,
        "crawl_interval_hours": settings.CRAWL_INTERVAL_HOURS,
        "default_company_id": settings.DEFAULT_COMPANY_ID
    }

@router.post("")
def update_settings(req: SettingsUpdate):
    if req.gemini_api_key is not None:
        settings.GEMINI_API_KEY = req.gemini_api_key
        os.environ["GEMINI_API_KEY"] = req.gemini_api_key
    if req.scheduler_timezone is not None:
        settings.SCHEDULER_TIMEZONE = req.scheduler_timezone
    if req.crawl_interval_hours is not None:
        settings.CRAWL_INTERVAL_HOURS = req.crawl_interval_hours

    return {"message": "Settings updated successfully", "gemini_configured": bool(settings.GEMINI_API_KEY)}
