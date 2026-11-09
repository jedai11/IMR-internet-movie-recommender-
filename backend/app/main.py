from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine, Base, SessionLocal
from app.db import models
from app.db.seed_data import seed_database
from app.api.api_router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed initial catalog
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Emotion-Grounded, Grounded Movie Recommender System based on Russell's Circumplex Model",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/health")
def health():
    has_key = bool(settings.GEMINI_API_KEY)
    masked_key = f"{settings.GEMINI_API_KEY[:6]}...{settings.GEMINI_API_KEY[-4:]}" if has_key else None
    return {
        "status": "healthy",
        "gemini_integrated": has_key,
        "gemini_key_preview": masked_key,
        "gemini_model": settings.GEMINI_MODEL,
        "database": "sqlite_connected"
    }

@app.get("/api/status")
def api_status():
    has_key = bool(settings.GEMINI_API_KEY)
    masked_key = f"{settings.GEMINI_API_KEY[:6]}...{settings.GEMINI_API_KEY[-4:]}" if has_key else None
    return {
        "system": "MoodReel Affective Recommendation Engine",
        "gemini_api_integrated": has_key,
        "gemini_key_preview": masked_key,
        "primary_model": settings.GEMINI_MODEL,
        "fallback_model": "gemini-3.5-flash",
        "status": "active"
    }

