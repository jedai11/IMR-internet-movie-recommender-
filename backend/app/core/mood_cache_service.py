"""
MOOD CACHE SERVICE

Provides persistent, single-fetch caching of TMDB discover results keyed by mood.
- Checks local SQLite database first (0 TMDB calls on cache hit).
- Uses concurrency locks so simultaneous uncached requests for the same mood do not duplicate TMDB calls.
- Configurable 7-day expiry and fallback to stale stored cache if TMDB fails or times out.
- Stores only: tmdb_id, title, poster_path, backdrop_path, release_year.
- Eliminates per-movie enrichment (details, credits, videos) entirely.
"""

import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.db.models import MoodMovieCache, utc_now
from app.core.tmdb_service import tmdb_service
from app.core.mood_tmdb_mapping import (
    DEFAULT_CACHE_EXPIRY_DAYS,
    MOOD_TMDB_MAPPING,
    resolve_mood_key,
    get_tmdb_query_params
)

logger = logging.getLogger(__name__)

# Concurrency locking: prevents duplicate TMDB calls for the same mood
_mood_locks: Dict[str, threading.Lock] = defaultdict(threading.Lock)
_meta_lock = threading.Lock()

def get_mood_lock(mood_key: str) -> threading.Lock:
    with _meta_lock:
        return _mood_locks[mood_key]


class MoodCacheService:
    def __init__(self, expiry_days: int = DEFAULT_CACHE_EXPIRY_DAYS):
        self.expiry_days = expiry_days

    def get_stored_mood_movies(
        self,
        mood_key: str,
        db: Session,
        include_expired: bool = False
    ) -> List[MoodMovieCache]:
        """
        Retrieves cached movies for a mood directly from SQLite.
        If include_expired is False, filters by expires_at > utc_now().
        """
        query = db.query(MoodMovieCache).filter(MoodMovieCache.mood_key == mood_key)
        if not include_expired:
            now = datetime.now(timezone.utc)
            query = query.filter(MoodMovieCache.expires_at > now)
        return query.order_by(MoodMovieCache.order_index.asc()).all()

    def fetch_and_store_from_tmdb(
        self,
        mood_key: str,
        db: Session,
        max_pages: int = 3,
        origin_keys: Optional[List[str]] = None,
        adult_mode: Optional[str] = "all",
        censorship: Optional[str] = "all",
        cache_key: Optional[str] = None
    ) -> List[MoodMovieCache]:
        """
        Calls TMDB /discover/movie endpoint concurrently for multiple pages (default 3 pages = ~60 movies)
        in parallel via ThreadPoolExecutor, achieving ~0.7-1.1s latency on uncached queries.
        Saves deduplicated results to the database keyed by cache_key and returns persisted objects.
        """
        storage_key = cache_key or mood_key
        logger.info(
            f"[MoodCache] Concurrently fetching {max_pages} discover pages from TMDB for key '{storage_key}' "
            f"(mood='{mood_key}', origins={origin_keys}, adult={adult_mode}, censorship={censorship})..."
        )

        def fetch_single_page(p: int):
            params = get_tmdb_query_params(
                mood_key,
                page=p,
                origin_keys=origin_keys,
                adult_mode=adult_mode,
                censorship=censorship
            )
            data = tmdb_service._execute_api_request("discover/movie", params)
            return p, data

        with ThreadPoolExecutor(max_workers=max_pages) as executor:
            page_outputs = list(executor.map(fetch_single_page, range(1, max_pages + 1)))

        # Preserve TMDB popularity ranking by sorting results by page number
        page_outputs.sort(key=lambda x: x[0])

        raw_results = []
        seen_ids = set()
        for _, discover_data in page_outputs:
            if not discover_data or not discover_data.get("results"):
                continue
            for m in discover_data["results"]:
                m_id = m.get("id")
                if m_id and m_id not in seen_ids:
                    seen_ids.add(m_id)
                    raw_results.append(m)

        if not raw_results:
            logger.warning(f"[MoodCache] TMDB discover returned no results for key '{storage_key}'.")
            return []

        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=self.expiry_days)

        # Clear existing cached entries for this cache key
        db.query(MoodMovieCache).filter(MoodMovieCache.mood_key == storage_key).delete()

        new_entries: List[MoodMovieCache] = []
        for idx, item in enumerate(raw_results):
            tmdb_id = item.get("id")
            title = item.get("title")
            if not tmdb_id or not title:
                continue

            release_date = item.get("release_date") or ""
            year = int(release_date[:4]) if len(release_date) >= 4 and release_date[:4].isdigit() else None

            cache_record = MoodMovieCache(
                mood_key=storage_key,
                tmdb_id=tmdb_id,
                title=title,
                poster_path=item.get("poster_path"),
                backdrop_path=item.get("backdrop_path"),
                release_year=year,
                order_index=idx,
                cached_at=now,
                expires_at=expires_at
            )
            new_entries.append(cache_record)

        db.add_all(new_entries)
        db.commit()

        logger.info(f"[MoodCache] Successfully stored {len(new_entries)} movies in parallel for key '{storage_key}' (Expires: {expires_at.date()}).")
        return new_entries

    def get_mood_recommendations(
        self,
        mood_key: str,
        db: Session,
        origin_keys: Optional[List[str]] = None,
        adult_mode: Optional[str] = "all",
        censorship: Optional[str] = "all",
        force_refresh: bool = False,
        limit: int = 36
    ) -> List[Dict[str, Any]]:
        """
        Primary Discovery Accessor:
        1. Resolves composite storage key (e.g. 'joyful:bollywood:adult_18_plus').
        2. Checks database for mood's stored results.
        3. If found, unexpired, and has sufficient results for requested limit, returns immediately (0 TMDB calls).
        4. If missing/expired/insufficient, acquires lock to fetch up to 3 pages (~60 movies).
        5. Re-checks DB inside lock (double-checked locking).
        6. Calls TMDB discover once, saves to DB, and returns results.
        7. If TMDB fails, falls back to stale stored results if any exist.
        """
        clean_key = mood_key.strip().lower()
        canonical_origins = sorted(list(set(origin_keys))) if origin_keys else []
        
        # Build composite storage key
        key_parts = [clean_key]
        if canonical_origins:
            key_parts.append('+'.join(canonical_origins))
        if adult_mode and adult_mode != "all":
            key_parts.append(f"adult_{adult_mode}")
        if censorship and censorship != "all":
            key_parts.append(f"censor_{censorship}")
        storage_key = ":".join(key_parts)

        origin_label = ", ".join([k.capitalize() for k in canonical_origins]) if canonical_origins else "TMDB"

        # Step 1: Check database (Cache Hit path - 0 TMDB calls)
        if not force_refresh:
            cached = self.get_stored_mood_movies(storage_key, db, include_expired=False)
            if cached and (len(cached) >= limit or len(cached) >= 30):
                logger.info(f"[MoodCache HIT] Serving {len(cached[:limit])} movies for key '{storage_key}' directly from DB (0 TMDB calls).")
                return self._format_results(cached[:limit], origin_label=origin_label)

        # Step 2: Missing or Expired - Acquire Lock
        lock = get_mood_lock(storage_key)
        with lock:
            # Double-check inside lock: another thread might have just fetched it
            if not force_refresh:
                cached = self.get_stored_mood_movies(storage_key, db, include_expired=False)
                if cached and (len(cached) >= limit or len(cached) >= 30):
                    logger.info(f"[MoodCache HIT (post-lock)] Serving {len(cached[:limit])} movies for key '{storage_key}' (0 TMDB calls).")
                    return self._format_results(cached[:limit], origin_label=origin_label)

            # Step 3: Fetch from TMDB discover endpoint (3 pages = ~60 movies)
            try:
                new_records = self.fetch_and_store_from_tmdb(
                    mood_key=clean_key,
                    db=db,
                    max_pages=3,
                    origin_keys=canonical_origins,
                    adult_mode=adult_mode,
                    censorship=censorship,
                    cache_key=storage_key
                )
                if new_records:
                    return self._format_results(new_records[:limit], origin_label=origin_label)
            except Exception as e:
                logger.error(f"[MoodCache] TMDB discover fetch failed for '{storage_key}': {e}")

            # Step 4: Fallback to stale stored results if TMDB fails or is unavailable
            stale_cached = self.get_stored_mood_movies(storage_key, db, include_expired=True)
            if stale_cached:
                logger.warning(f"[MoodCache FALLBACK] TMDB failed; serving {len(stale_cached)} stale stored movies for '{storage_key}'.")
                return self._format_results(stale_cached[:limit], origin_label=origin_label)

            return []

    def refresh_mood(
        self,
        mood_key: str,
        db: Session,
        origin_keys: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Manual 'refresh mood' command: bypasses cache and re-fetches from TMDB discover.
        """
        clean_key = mood_key.strip().lower()
        return self.get_mood_recommendations(clean_key, db, origin_keys=origin_keys, force_refresh=True)

    def _format_results(self, records: List[MoodMovieCache], origin_label: str = "TMDB") -> List[Dict[str, Any]]:
        """
        Formats stored DB records into response objects with dynamic TMDB image URLs.
        Image base URL is retrieved from TMDB's /configuration endpoint and cached.
        Uses w342 for high-density, fast-loading responsive posters (3x faster than w500).
        """
        poster_base = tmdb_service.get_image_base_url(size="w342")
        backdrop_base = tmdb_service.get_image_base_url(size="w780")

        results = []
        for r in records:
            poster_url = f"{poster_base}{r.poster_path.lstrip('/')}" if r.poster_path else None
            backdrop_url = f"{backdrop_base}{r.backdrop_path.lstrip('/')}" if r.backdrop_path else None

            results.append({
                "tmdb_id": r.tmdb_id,
                "title_id": f"tmdb_{r.tmdb_id}",
                "title": r.title,
                "release_year": r.release_year,
                "poster_path": r.poster_path,
                "poster_url": poster_url,
                "backdrop_path": r.backdrop_path,
                "backdrop_url": backdrop_url,
                "tmdb_url": f"https://www.themoviedb.org/movie/{r.tmdb_id}",
                "origin": origin_label
            })
        return results


mood_cache_service = MoodCacheService()

