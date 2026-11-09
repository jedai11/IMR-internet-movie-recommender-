import sys
import os
import time
import json
from datetime import datetime, timezone
from typing import List, Dict, Any

# Ensure backend path is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import event
from sqlalchemy.engine import Engine
import httpx

from app.db.session import engine, SessionLocal
from app.db.models import MoodMovieCache
from app.core.mood_cache_service import mood_cache_service
from app.core.tmdb_service import tmdb_service
from app.schemas.recommendation import RecommendationRequest, FilterCriteria
from app.api.routers.recommend import get_recommendations

# Global SQL Query Logger
sql_queries: List[Dict[str, Any]] = []

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.perf_counter()

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_ms = (time.perf_counter() - context._query_start_time) * 1000.0
    sql_queries.append({
        "statement": statement.strip().replace("\n", " "),
        "duration_ms": total_ms
    })


def run_measurements():
    print("=" * 80)
    print("STARTING DETAILED PERFORMANCE PROFILING & MEASUREMENT")
    print("=" * 80)

    db = SessionLocal()
    test_mood = "fearful"  # A fresh test mood
    
    # 0. Clean DB cache for this test mood to ensure true uncached first run
    db.query(MoodMovieCache).filter(MoodMovieCache.mood_key.like(f"{test_mood}%")).delete()
    db.commit()

    # Reset logs
    tmdb_service.http_call_logs.clear()
    sql_queries.clear()

    # --------------------------------------------------------------------------
    # CASE A: First request for a mood (Uncached)
    # --------------------------------------------------------------------------
    print("\n[Measuring Case A: First request (uncached)]...")
    req_a = RecommendationRequest(
        session_id="profile_session_1",
        mood_name=test_mood,
        filters=FilterCriteria(),
        limit=36
    )

    t0_a = time.perf_counter()
    resp_a = get_recommendations(request=req_a, db=db)
    t1_a = time.perf_counter()
    total_time_a = (t1_a - t0_a) * 1000.0

    tmdb_calls_a = list(tmdb_service.http_call_logs)
    db_queries_a = list(sql_queries)
    
    # Check cache write
    stored_records_a = db.query(MoodMovieCache).filter(MoodMovieCache.mood_key == test_mood).all()

    # --------------------------------------------------------------------------
    # CASE B: Second request for the same mood (Should be Cached)
    # --------------------------------------------------------------------------
    print("[Measuring Case B: Second request (cached)]...")
    tmdb_service.http_call_logs.clear()
    sql_queries.clear()

    req_b = RecommendationRequest(
        session_id="profile_session_2",
        mood_name=test_mood,
        filters=FilterCriteria(),
        limit=36
    )

    t0_b = time.perf_counter()
    resp_b = get_recommendations(request=req_b, db=db)
    t1_b = time.perf_counter()
    total_time_b = (t1_b - t0_b) * 1000.0

    tmdb_calls_b = list(tmdb_service.http_call_logs)
    db_queries_b = list(sql_queries)

    # --------------------------------------------------------------------------
    # CASE C: Full page load including images
    # --------------------------------------------------------------------------
    print("[Measuring Case C: Full page load including image assets]...")
    recs = resp_b.recommendations
    image_urls = [r.poster_url for r in recs if r.poster_url]

    img_start = time.perf_counter()
    img_results = []
    total_bytes = 0

    # Measure loading of images as client browser does (concurrently or in chunks)
    with httpx.Client(timeout=10.0, follow_redirects=True) as client:
        for idx, url in enumerate(image_urls):
            single_t0 = time.perf_counter()
            try:
                r = client.get(url)
                dur = (time.perf_counter() - single_t0) * 1000.0
                size = len(r.content)
                total_bytes += size
                img_results.append({
                    "url": url,
                    "status": r.status_code,
                    "size_bytes": size,
                    "duration_ms": dur
                })
            except Exception as e:
                img_results.append({
                    "url": url,
                    "status": "error",
                    "error": str(e),
                    "size_bytes": 0,
                    "duration_ms": (time.perf_counter() - single_t0) * 1000.0
                })

    img_end = time.perf_counter()
    total_img_time = (img_end - img_start) * 1000.0
    case_c_total = total_time_b + total_img_time

    # --------------------------------------------------------------------------
    # CHECKS & VERIFICATIONS
    # --------------------------------------------------------------------------
    # 3. Check whether enrich_movie or per-movie calls ran
    any_enrich_calls = any(
        "movie/" in str(call.get("endpoint", "")) and not "discover" in str(call.get("endpoint", ""))
        for call in tmdb_calls_a + tmdb_calls_b
    )

    # 4. Check cache key consistency
    cache_key_write = test_mood
    cache_key_read = resp_b.meta.get("mood_key")
    cache_key_identical = (cache_key_write == cache_key_read)
    is_expired = False
    now = datetime.now(timezone.utc)
    for rec in stored_records_a:
        exp = rec.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp < now:
            is_expired = True

    # --------------------------------------------------------------------------
    # OUTPUT STRUCTURED REPORT
    # --------------------------------------------------------------------------
    report = {
        "case_a_uncached": {
            "total_time_ms": round(total_time_a, 2),
            "tmdb_calls_count": len(tmdb_calls_a),
            "tmdb_calls_duration_ms": round(sum(c.get("duration_ms", 0) for c in tmdb_calls_a), 2),
            "tmdb_calls_detail": [
                {
                    "endpoint": c.get("endpoint"),
                    "page": c.get("params", {}).get("page"),
                    "duration_ms": round(c.get("duration_ms", 0), 2),
                    "status": c.get("status_code"),
                    "retried": c.get("was_retried")
                }
                for c in tmdb_calls_a
            ],
            "db_queries_count": len(db_queries_a),
            "db_queries_total_ms": round(sum(q["duration_ms"] for q in db_queries_a), 2),
            "db_queries_detail": [
                {"statement": q["statement"][:90] + "...", "duration_ms": round(q["duration_ms"], 2)}
                for q in db_queries_a
            ],
            "movies_returned": len(resp_a.recommendations)
        },
        "case_b_cached": {
            "total_time_ms": round(total_time_b, 2),
            "tmdb_calls_count": len(tmdb_calls_b),
            "tmdb_calls_duration_ms": round(sum(c.get("duration_ms", 0) for c in tmdb_calls_b), 2),
            "db_queries_count": len(db_queries_b),
            "db_queries_total_ms": round(sum(q["duration_ms"] for q in db_queries_b), 2),
            "db_queries_detail": [
                {"statement": q["statement"][:90] + "...", "duration_ms": round(q["duration_ms"], 2)}
                for q in db_queries_b
            ],
            "movies_returned": len(resp_b.recommendations)
        },
        "case_c_full_page_with_images": {
            "total_time_ms": round(case_c_total, 2),
            "api_response_ms": round(total_time_b, 2),
            "images_download_total_ms": round(total_img_time, 2),
            "images_count": len(img_results),
            "images_total_kb": round(total_bytes / 1024.0, 2),
            "images_avg_kb": round((total_bytes / len(img_results)) / 1024.0, 2) if img_results else 0,
            "images_avg_duration_ms": round(total_img_time / len(img_results), 2) if img_results else 0
        },
        "checks": {
            "enrich_movie_on_request_path": any_enrich_calls,
            "cache_key_write": cache_key_write,
            "cache_key_read": cache_key_read,
            "cache_key_identical": cache_key_identical,
            "cached_data_expired": is_expired,
            "cached_data_ignored": (len(tmdb_calls_b) > 0)
        }
    }

    print("\n--- RESULTS JSON ---")
    print(json.dumps(report, indent=2))

    db.close()

if __name__ == "__main__":
    run_measurements()

