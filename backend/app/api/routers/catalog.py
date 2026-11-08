import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.db.models import MovieTitle, Genre, ContentWarning, TMDBMovieQueue, TMDBMovieStack
from app.core.tmdb_service import tmdb_service, POSTER_CACHE_DIR

router = APIRouter(prefix="/catalog", tags=["catalog"])

@router.get("/titles")
def get_catalog_titles(db: Session = Depends(get_db)):
    """
    Returns high-level catalog overview with emotion coordinates.
    """
    titles = db.query(MovieTitle).all()
    results = []
    for m in titles:
        results.append({
            "id": m.id,
            "title": m.title,
            "year": m.release_year,
            "runtime": m.runtime_minutes,
            "poster_url": f"/api/catalog/poster/{m.id}",
            "valence": m.valence_score,
            "arousal": m.arousal_score,
            "origin": getattr(m, "origin", "Hollywood") or "Hollywood",
            "genres": [g.name for g in m.genres],
            "platforms": [av.platform for av in m.availabilities],
            "warnings": [
                {"code": cw.warning_code, "status": cw.status}
                for cw in m.content_warnings
            ]
        })
    return {"total": len(results), "titles": results}

@router.get("/poster/{title_id}")
def get_movie_poster(title_id: str, db: Session = Depends(get_db)):
    """
    Serves the authentic high-resolution theatrical movie poster directly from local storage.
    If not yet cached locally, automatically queries TMDB, downloads the official poster, caches it, and serves it.
    """
    cached_path = os.path.join(POSTER_CACHE_DIR, f"{title_id}.jpg")
    if os.path.exists(cached_path) and os.path.getsize(cached_path) > 1000:
        return FileResponse(
            cached_path, 
            media_type="image/jpeg", 
            headers={"Cache-Control": "public, max-age=86400"}
        )

    movie = db.query(MovieTitle).filter(MovieTitle.id == title_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # On-demand TMDB poster resolution
    downloaded_path = tmdb_service.fetch_and_cache_poster(
        title=movie.title,
        release_year=movie.release_year,
        title_id=movie.id
    )
    if downloaded_path and os.path.exists(downloaded_path) and os.path.getsize(downloaded_path) > 1000:
        return FileResponse(
            downloaded_path,
            media_type="image/jpeg",
            headers={"Cache-Control": "public, max-age=86400"}
        )
        
    raise HTTPException(status_code=404, detail="Poster not available")

@router.get("/tmdb-status")
def get_tmdb_status(db: Session = Depends(get_db)):
    """
    Diagnostic endpoint to verify TMDB integration:
    - Verifies API key is active
    - Performs live ping to TMDB
    - Checks cache status across catalog movies
    """
    titles = db.query(MovieTitle).all()
    total_titles = len(titles)
    cached_count = 0
    missing_sample = []

    for m in titles:
        path = os.path.join(POSTER_CACHE_DIR, f"{m.id}.jpg")
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            cached_count += 1
        elif len(missing_sample) < 5:
            missing_sample.append({"id": m.id, "title": m.title, "year": m.release_year})

    # Test live TMDB query
    test_lookup = tmdb_service.search_movie_or_tv("Inception", 2010)
    connected = test_lookup is not None

    return {
        "status": "connected" if connected else "error",
        "api_key_configured": bool(tmdb_service.api_key),
        "api_key_masked": f"{tmdb_service.api_key[:6]}...{tmdb_service.api_key[-4:]}" if tmdb_service.api_key else None,
        "live_api_ping": "success" if connected else "failed",
        "sample_test_query": {
            "query": "Inception (2010)",
            "tmdb_title": test_lookup.get("title") if test_lookup else None,
            "tmdb_poster_path": test_lookup.get("poster_path") if test_lookup else None,
            "tmdb_rating": test_lookup.get("vote_average") if test_lookup else None
        } if test_lookup else None,
        "poster_cache": {
            "cached_posters": cached_count,
            "total_titles": total_titles,
            "cache_coverage_percentage": round((cached_count / total_titles * 100), 1) if total_titles else 0,
            "missing_sample": missing_sample
        }
    }

@router.get("/stats")
def get_catalog_stats(db: Session = Depends(get_db)):
    """
    Returns catalog distribution metrics.
    """
    titles = db.query(MovieTitle).all()
    genres = db.query(Genre).all()
    warnings = db.query(ContentWarning).all()

    avg_v = sum(m.valence_score for m in titles) / len(titles) if titles else 0.0
    avg_a = sum(m.arousal_score for m in titles) / len(titles) if titles else 0.0

    return {
        "total_titles": len(titles),
        "total_genres": len(genres),
        "total_warning_records": len(warnings),
        "average_valence": round(avg_v, 3),
        "average_arousal": round(avg_a, 3),
        "platforms_supported": ["netflix", "prime", "hulu", "max", "apple_tv", "paramount", "free"]
    }

@router.get("/stack-queue-status")
def get_stack_queue_status(db: Session = Depends(get_db)):
    """
    Returns live inspection data for the TMDB FIFO Queue and LIFO Stack database:
    - Verifies movies are queued, ingested into SQLite DB, and tracked in the stack
    - Shows that previously abstracted movies are re-used directly with 0 TMDB calls
    """
    total_queued = db.query(TMDBMovieQueue).count()
    processed_count = db.query(TMDBMovieQueue).filter(TMDBMovieQueue.status == "PROCESSED").count()
    pending_count = db.query(TMDBMovieQueue).filter(TMDBMovieQueue.status == "QUEUED").count()
    
    recent_queue = (
        db.query(TMDBMovieQueue)
        .order_by(TMDBMovieQueue.id.desc())
        .limit(5)
        .all()
    )

    total_stack_items = db.query(TMDBMovieStack).count()
    recent_stack = (
        db.query(TMDBMovieStack)
        .order_by(TMDBMovieStack.stack_order.desc())
        .limit(5)
        .all()
    )

    return {
        "fifo_queue": {
            "total_items_recorded": total_queued,
            "processed_into_db": processed_count,
            "pending_in_queue": pending_count,
            "recent_queued_movies": [
                {"tmdb_id": q.tmdb_id, "title": q.title, "genre": q.genre_name, "status": q.status}
                for q in recent_queue
            ]
        },
        "lifo_stack": {
            "total_stack_entries": total_stack_items,
            "recent_top_of_stack": [
                {"title_id": s.title_id, "genre": s.genre_name, "order": s.stack_order}
                for s in recent_stack
            ]
        }
    }
