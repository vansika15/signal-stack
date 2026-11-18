import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Signal Stack Intelligence Engine"
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./signal_stack.db"
    GEMINI_API_KEY: Optional[str] = None
    SCHEDULER_ENABLED: bool = True
    SCHEDULER_TIMEZONE: str = "UTC"
    CRAWL_INTERVAL_HOURS: int = 24
    DEFAULT_COMPANY_ID: str = "meetuniversity"
    
    # Server & CORS
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "*"
    
    # Scheduling CRON
    WEEKLY_REPORT_CRON_DAY: str = "mon"
    WEEKLY_REPORT_CRON_HOUR: int = 8
    WEEKLY_REPORT_CRON_MINUTE: int = 0
    MONTHLY_AUDIT_DAY: int = 1
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
