import os
import json
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.models import MovieTitle, Genre, Availability, TMDBMovieQueue, TMDBMovieStack
from app.core.tmdb_service import tmdb_service

logger = logging.getLogger(__name__)

# TMDB Genre ID mapping
TMDB_GENRE_MAP: Dict[str, int] = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "horror": 27,
    "music": 10402,
    "mystery": 9648,
    "romance": 10749,
    "sci-fi": 878,
    "science fiction": 878,
    "thriller": 53,
    "war": 10752,
    "western": 37
}

# Default emotional affect coordinates by genre on Russell's Circumplex (valence, arousal)
GENRE_AFFECT_MAP: Dict[str, tuple[float, float]] = {
    "horror": (-0.75, 0.85),
    "thriller": (-0.45, 0.75),
    "action": (0.35, 0.80),
    "comedy": (0.75, 0.60),
    "romance": (0.70, 0.35),
    "drama": (-0.20, 0.25),
    "sci-fi": (0.25, 0.65),
    "science fiction": (0.25, 0.65),
    "animation": (0.80, 0.50),
    "family": (0.75, 0.45),
    "adventure": (0.45, 0.70),
    "fantasy": (0.40, 0.60),
    "crime": (-0.35, 0.60),
    "mystery": (-0.30, 0.55),
    "documentary": (0.10, 0.10),
    "history": (0.05, 0.20),
    "war": (-0.60, 0.70),
    "music": (0.65, 0.55),
    "western": (0.00, 0.50)
}


class StackQueueMovieManager:
    """
    Manages dynamic Just-In-Time (JIT) abstraction from TMDB:
    - FIFO Queue: Buffers new candidate movies discovered from TMDB for a requested genre.
    - Persistent SQLite DB: Permanently caches movies, genres, and posters so they NEVER need to be extracted again.
    - LIFO Stack: Tracks active recommendation sequence and provides instantaneous retrieval.
    """

    def __init__(self):
        self.processed_tmdb_ids: set[int] = set()

    def get_genre_id(self, genre_name: str) -> Optional[int]:
        clean = genre_name.strip().lower()
        return TMDB_GENRE_MAP.get(clean)

    def is_movie_cached_in_db(self, title: str, db: Session) -> bool:
        """Checks if movie already exists in the local database."""
        clean = title.strip().lower()
        exists = db.query(MovieTitle).filter(MovieTitle.title.ilike(f"%{clean}%")).first()
        return exists is not None

    def push_to_fifo_queue(self, tmdb_id: int, title: str, genre_name: str, payload: dict, db: Session) -> TMDBMovieQueue:
        """Pushes a candidate movie into the persistent FIFO queue."""
        queue_item = TMDBMovieQueue(
            tmdb_id=tmdb_id,
            title=title,
            genre_name=genre_name.capitalize(),
            status="QUEUED",
            payload_json=json.dumps(payload),
            queued_at=datetime.now(timezone.utc)
        )
        db.add(queue_item)
        db.commit()
        db.refresh(queue_item)
        return queue_item

    def dequeue_and_ingest(self, db: Session) -> Optional[MovieTitle]:
        """
        Dequeues the oldest candidate (FIFO) from the queue, abstracts full details from TMDB,
        persists it into MovieTitle, and marks queue status as PROCESSED.
        """
        queue_item = (
            db.query(TMDBMovieQueue)
            .filter(TMDBMovieQueue.status == "QUEUED")
            .order_by(TMDBMovieQueue.id.asc())
            .first()
        )
        if not queue_item:
            return None

        payload = json.loads(queue_item.payload_json or "{}")
        tmdb_id = queue_item.tmdb_id
        title = queue_item.title
        primary_genre_name = queue_item.genre_name

        # Deduplicate check: if title already in DB, simply mark processed
        existing = db.query(MovieTitle).filter(MovieTitle.title.ilike(title)).first()
        if existing:
            queue_item.status = "PROCESSED"
            queue_item.processed_at = datetime.now(timezone.utc)
            db.commit()
            return existing

        # Fetch enriched TMDB details (cast, director, trailer, backdrop, runtime)
        details = tmdb_service.get_details(tmdb_id, payload.get("media_type", "movie"))
        runtime = (details.get("runtime") if details else None) or payload.get("runtime", 115)
        release_date = payload.get("release_date") or ""
        year = int(release_date[:4]) if len(release_date) >= 4 and release_date[:4].isdigit() else 2020

        # Calculate Affective Coordinates (Russell's Circumplex)
        v, a = GENRE_AFFECT_MAP.get(primary_genre_name.lower(), (0.2, 0.4))
        vote_avg = float(payload.get("vote_average", 7.0) or 7.0)

        # Generate a unique slug ID
        title_slug = f"tmdb_{tmdb_id}"

        new_movie = MovieTitle(
            id=title_slug,
            title=title,
            release_year=year,
            runtime_minutes=runtime if runtime and runtime > 30 else 110,
            synopsis=payload.get("overview") or (details.get("overview") if details else ""),
            valence_score=round(v, 2),
            arousal_score=round(a, 2),
            valence_arousal_source="tmdb_genre_circumplex_model",
            valence_arousal_confidence=0.88,
            popularity_score=vote_avg,
            origin="Hollywood" if payload.get("original_language") == "en" else "World Cinema"
        )

        # Attach genres
        genre_obj = db.query(Genre).filter(Genre.name.ilike(primary_genre_name)).first()
        if not genre_obj:
            genre_obj = Genre(name=primary_genre_name.capitalize())
            db.add(genre_obj)
            db.flush()
        new_movie.genres.append(genre_obj)

        # Attach streaming availability
        new_movie.availabilities.append(Availability(title_id=title_slug, platform="free", region="GLOBAL"))
        new_movie.availabilities.append(Availability(title_id=title_slug, platform="prime", region="GLOBAL"))

        db.add(new_movie)

        # Mark queue item PROCESSED
        queue_item.status = "PROCESSED"
        queue_item.processed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(new_movie)

        # Prefetch poster asynchronously/locally
        if payload.get("poster_path"):
            tmdb_service.fetch_and_cache_poster(title, year, title_slug)

        logger.info(f"Ingested from TMDB queue -> DB: '{title}' ({year})")
        return new_movie

    def abstract_genre_from_tmdb(self, genre_name: str, db: Session, target_count: int = 5) -> List[MovieTitle]:
        """
        When user asks for a genre:
        1. Checks how many movies of this genre already exist in the database.
        2. If more are needed, queries TMDB discover endpoint.
        3. Pushes new movies to FIFO Queue.
        4. Dequeues and commits them to the database.
        5. Future queries for this genre will find them in DB and NEVER hit TMDB again!
        """
        clean_genre = genre_name.strip()
        genre_id = self.get_genre_id(clean_genre)

        # 1. First check existing in SQLite database
        existing_matches = (
            db.query(MovieTitle)
            .join(MovieTitle.genres)
            .filter(Genre.name.ilike(f"%{clean_genre}%"))
            .all()
        )

        if len(existing_matches) >= target_count:
            logger.info(f"Using {len(existing_matches)} cached DB movies for genre '{clean_genre}' (0 TMDB calls)")
            return existing_matches

        # 2. If we need fresh movies and have a valid TMDB genre ID
        if not genre_id:
            return existing_matches

        logger.info(f"Abstracting fresh movies for genre '{clean_genre}' (TMDB ID: {genre_id})")
        discover_data = tmdb_service._execute_api_request("discover/movie", {
            "with_genres": genre_id,
            "sort_by": "popularity.desc",
            "vote_count.gte": 150,
            "page": 1
        })

        if not discover_data or not discover_data.get("results"):
            return existing_matches

        results = discover_data["results"]
        newly_ingested = []

        for item in results:
            t_id = item.get("id")
            title = item.get("title")
            if not t_id or not title:
                continue

            # If already in DB, skip
            if self.is_movie_cached_in_db(title, db):
                continue

            # Push to FIFO Queue
            self.push_to_fifo_queue(t_id, title, clean_genre, item, db)

            # Dequeue and persist into SQLite database
            movie = self.dequeue_and_ingest(db)
            if movie:
                newly_ingested.append(movie)

            if len(existing_matches) + len(newly_ingested) >= target_count + 6:
                break

        return existing_matches + newly_ingested

    def push_to_lifo_stack(self, title_id: str, genre_name: str, session_id: Optional[str], db: Session):
        """
        Pushes a recommended movie onto the active LIFO Stack for rapid retrieval
        and session history tracking.
        """
        try:
            # Determine current top stack order
            top_item = (
                db.query(TMDBMovieStack)
                .filter(TMDBMovieStack.genre_name == genre_name.capitalize())
                .order_by(TMDBMovieStack.stack_order.desc())
                .first()
            )
            next_order = (top_item.stack_order + 1) if top_item else 1

            stack_item = TMDBMovieStack(
                session_id=session_id or "default_session",
                title_id=title_id,
                genre_name=genre_name.capitalize(),
                stack_order=next_order,
                pushed_at=datetime.now(timezone.utc)
            )
            db.add(stack_item)
            db.commit()
        except Exception as e:
            logger.error(f"Failed to push to LIFO stack: {e}")
            db.rollback()

    def get_genre_lifo_stack(self, genre_name: str, db: Session, limit: int = 10) -> List[MovieTitle]:
        """
        Retrieves the most recently pushed movies (LIFO) for this genre from the stack.
        Zero TMDB calls - served entirely from the local stack and database!
        """
        clean = genre_name.strip().capitalize()
        stack_records = (
            db.query(TMDBMovieStack)
            .filter(TMDBMovieStack.genre_name == clean)
            .order_by(TMDBMovieStack.stack_order.desc())
            .limit(limit)
            .all()
        )
        return [item.title for item in stack_records if item.title]


stack_queue_manager = StackQueueMovieManager()

