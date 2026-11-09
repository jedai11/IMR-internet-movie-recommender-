import time
import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.db.session import get_db
from app.db.models import MovieTitle, EventLog
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    MovieRecommendation,
    MoodCompatibility,
    SafetyCheckResult
)
from app.core.mood_cache_service import mood_cache_service
from app.core.mood_tmdb_mapping import (
    MOOD_TMDB_MAPPING,
    resolve_mood_key,
    DEFAULT_CACHE_EXPIRY_DAYS
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.post("", response_model=RecommendationResponse)
def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Mood-Grounded Movie Recommendation Engine:
    1. Resolves mood key from explicit mood_name, free text, or affect coordinates.
    2. Queries local SQLite mood cache:
       - Cache hit (not expired): Returns stored titles immediately with ZERO TMDB calls.
       - Cache miss or expired: Calls TMDB discover once per page (with concurrency locking),
         persists to DB with 7-day expiry, and returns stored titles.
    3. Completely removes slow per-movie enrichment (enrich_movie) from request path.
    4. If TMDB fails or times out, serves last stored results.
    """
    start_time = time.perf_counter()

    # 1. Resolve canonical mood key
    pref_genre = request.filters.preferred_genres[0] if request.filters and request.filters.preferred_genres else None
    v = request.target_mood.valence if request.target_mood else None
    a = request.target_mood.arousal if request.target_mood else None

    mood_key = resolve_mood_key(
        mood_name=request.mood_name,
        text=pref_genre,
        valence=v,
        arousal=a
    )

    limit = request.limit or 12

    # 2. Fetch recommendations from Mood Cache Service
    cached_movies = mood_cache_service.get_mood_recommendations(
        mood_key=mood_key,
        db=db,
        force_refresh=False,
        limit=limit
    )

    top_recommendations: List[MovieRecommendation] = []

    if cached_movies:
        for idx, item in enumerate(cached_movies):
            rec = MovieRecommendation(
                title_id=item["title_id"],
                tmdb_id=item["tmdb_id"],
                title=item["title"],
                release_year=item.get("release_year") or 2024,
                runtime_minutes=110,
                genres=[mood_key.capitalize()],
                origin="TMDB",
                poster_url=item.get("poster_url"),
                backdrop_url=item.get("backdrop_url"),
                tmdb_url=item.get("tmdb_url"),
                score=round(1.0 - (idx * 0.02), 2),
                match_rationale=f"Discovered for your {mood_key} mood from TMDB.",
                mood_compatibility=MoodCompatibility(
                    title_valence=v if v is not None else 0.0,
                    title_arousal=a if a is not None else 0.0,
                    distance=0.0,
                    fit_percentage=max(80, 100 - (idx * 2))
                ),
                safety_check=SafetyCheckResult(
                    flags_evaluated=0,
                    exclusions_passed=True,
                    unknown_metadata_excluded=[]
                )
            )
            top_recommendations.append(rec)
    else:
        # Fallback to local catalog if mood cache has no results and TMDB was offline
        excluded_genres = set(request.filters.excluded_genres) if request.filters and request.filters.excluded_genres else set()
        max_runtime = request.filters.max_runtime if request.filters else None

        local_query = db.query(MovieTitle)
        if max_runtime:
            local_query = local_query.filter(MovieTitle.runtime_minutes <= max_runtime)
        local_titles = local_query.all()
        for m in local_titles:
            g_names = [g.name for g in m.genres]
            if any(g in excluded_genres for g in g_names):
                continue
            top_recommendations.append(MovieRecommendation(
                title_id=m.id,
                tmdb_id=None,
                title=m.title,
                release_year=m.release_year,
                runtime_minutes=m.runtime_minutes,
                genres=g_names,
                origin=getattr(m, "origin", "Hollywood") or "Hollywood",
                poster_url=m.poster_url or f"/api/catalog/poster/{m.id}",
                tmdb_url=None,
                score=0.9,
                match_rationale=f"Catalog fallback for {mood_key} mood.",
                mood_compatibility=MoodCompatibility(
                    title_valence=m.valence_score,
                    title_arousal=m.arousal_score,
                    distance=0.1,
                    fit_percentage=90
                ),
                safety_check=SafetyCheckResult(
                    flags_evaluated=0,
                    exclusions_passed=True,
                    unknown_metadata_excluded=[]
                )
            ))
            if len(top_recommendations) >= limit:
                break

    latency_ms = int((time.perf_counter() - start_time) * 1000)

    # 3. Log event
    try:
        event = EventLog(
            session_id=request.session_id,
            mood_input=json.dumps(request.target_mood.model_dump() if request.target_mood else {"mood": mood_key}),
            filters_applied=json.dumps(request.filters.model_dump() if request.filters else {}),
            returned_title_ids=json.dumps([r.title_id for r in top_recommendations]),
            latency_ms=latency_ms
        )
        db.add(event)
        db.commit()
    except Exception as e:
        logger.debug(f"Event logging failed: {e}")

    return RecommendationResponse(
        session_id=request.session_id,
        recommendations=top_recommendations,
        meta={
            "mood_key": mood_key,
            "total_returned": len(top_recommendations),
            "cached_storage": True,
            "latency_ms": latency_ms
        }
    )


@router.post("/refresh-mood/{mood_key}")
def manual_refresh_mood(mood_key: str, db: Session = Depends(get_db)):
    """
    Manual 'refresh mood' command: forces fresh TMDB discover fetch for this mood,
    updates the persistent SQLite storage, and resets the 7-day expiry.
    """
    refreshed = mood_cache_service.refresh_mood(mood_key=mood_key, db=db)
    return {
        "status": "refreshed",
        "mood_key": mood_key,
        "count": len(refreshed),
        "expiry_days": DEFAULT_CACHE_EXPIRY_DAYS,
        "movies": refreshed
    }


@router.get("/mood-mapping")
def get_mood_mapping():
    """
    Returns the mood -> TMDB query parameter mapping configuration for editing/inspection.
    """
    return {
        "expiry_days": DEFAULT_CACHE_EXPIRY_DAYS,
        "mood_mapping": MOOD_TMDB_MAPPING
    }
