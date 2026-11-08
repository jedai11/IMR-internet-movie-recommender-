import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.db.models import MovieTitle, Genre, ContentWarning

router = APIRouter(prefix="/catalog", tags=["catalog"])

POSTER_CACHE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
    "poster_cache"
)

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
    Eliminates all CORS, referrer, and hotlinking restrictions.
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
        
    raise HTTPException(status_code=404, detail="Poster not available")

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
