import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .config import settings
from .database import engine, Base, SessionLocal
from .services.seed_service import seed_database
from .services.scheduler_service import SchedulerService

# Routers
from .routers import (
    companies,
    profiles,
    interviews,
    competitors,
    sources,
    crawler,
    intelligence,
    internal_docs,
    reports,
    scheduler,
    settings as settings_router
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("signal-stack")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize DB tables
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed default companies (MeetUniversity, Stripe, Datadog)
    logger.info("Seeding demonstration companies...")
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    # 3. Start background automation scheduler
    if settings.SCHEDULER_ENABLED and not os.environ.get("TESTING"):
        logger.info("Starting background scheduler...")
        SchedulerService.init_scheduler()

    yield

    # Shutdown
    if SchedulerService.scheduler and SchedulerService.scheduler.running:
        SchedulerService.scheduler.shutdown()

app = FastAPI(
    title="Signal Stack API",
    description="Autonomous Competitive & Market Intelligence System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(companies.router)
app.include_router(profiles.router)
app.include_router(interviews.router)
app.include_router(competitors.router)
app.include_router(sources.router)
app.include_router(crawler.router)
app.include_router(intelligence.router)
app.include_router(internal_docs.router)
app.include_router(reports.router)
app.include_router(scheduler.router)
app.include_router(settings_router.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "scheduler": SchedulerService.scheduler is not None and SchedulerService.scheduler.running
    }

# Mount static frontend production build if present
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static-frontend")
else:
    @app.get("/")
    def root():
        return {
            "status": "online",
            "service": "Signal Stack Autonomous Intelligence Engine",
            "version": "1.0.0",
            "docs_url": "/docs"
        }
