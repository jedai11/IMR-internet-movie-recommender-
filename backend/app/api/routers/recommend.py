import time
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db.models import MovieTitle, UserRating, EventLog
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    MovieRecommendation,
    MoodCompatibility,
    SafetyCheckResult
)
from app.core.filters import apply_hard_filters
from app.core.weighting import get_recommendation_weights
from app.core.ranking import rank_candidates
from app.core.llm_service import llm_service

router = APIRouter(prefix="/recommend", tags=["recommend"])

@router.post("", response_model=RecommendationResponse)
def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Core Grounded Recommendation Engine:
    1. Loads candidates from verified catalog DB.
    2. Identifies user's interaction history for cold-start weighting.
    3. Executes deterministic hard exclusion filters (including UNKNOWN-metadata defense).
    4. Ranks surviving candidates via Euclidean distance in Circumplex affect space.
    5. Generates grounded rationale for top matches.
    6. Logs event for metrics & auditability.
    """
    start_time = time.time()

    # 1. Fetch user history
    user_ratings = db.query(UserRating).filter(UserRating.session_id == request.session_id).all()
    seen_ids = {r.title_id for r in user_ratings}
    liked_genre_names = set()
    disliked_genre_names = set()

    for r in user_ratings:
        if r.title:
            g_names = {g.name.lower() for g in r.title.genres}
            if r.feedback_action in ("helped", "watched"):
                liked_genre_names.update(g_names)
            elif r.feedback_action in ("disliked", "thumbs_down"):
                disliked_genre_names.update(g_names)

    # 2. Query candidates from DB
    all_candidates = db.query(MovieTitle).all()

    # 3. Apply Hard Filters
    surviving_candidates, filter_audit = apply_hard_filters(
        candidates=all_candidates,
        filters=request.filters,
        seen_title_ids=seen_ids
    )

    # 4. Weight Calculation (Cold-start vs. Established)
    weights = get_recommendation_weights(interaction_count=len(user_ratings))

    # 5. Extract preferred genres (from semantics or explicit user preference)
    preferred_genre_names = set(request.filters.preferred_genres) if request.filters and request.filters.preferred_genres else set()

    # 6. Deterministic Ranking
    ranked_tuples = rank_candidates(
        candidates=surviving_candidates,
        target_mood=request.target_mood,
        weights=weights,
        liked_genre_names=liked_genre_names,
        disliked_genre_names=disliked_genre_names,
        preferred_genre_names=preferred_genre_names
    )

    # Select top K
    top_matches = ranked_tuples[:request.limit]
    top_recommendations: List[MovieRecommendation] = []

    for movie, score, detail in top_matches:
        genre_names = [g.name for g in movie.genres]
        platforms = [av.platform for av in movie.availabilities]
        
        # Grounded LLM Rationale Generation with semantic genre match acknowledgement
        rationale = llm_service.generate_rationale(
            movie_title=movie.title,
            genres=genre_names,
            valence=movie.valence_score,
            arousal=movie.arousal_score,
            strategy=request.strategy,
            target_mood=request.target_mood,
            matched_preferred_genre=detail.get("matched_preferred_genre")
        )

        rec = MovieRecommendation(
            title_id=movie.id,
            title=movie.title,
            release_year=movie.release_year,
            runtime_minutes=movie.runtime_minutes,
            genres=genre_names,
            poster_url=f"/api/catalog/poster/{movie.id}",
            synopsis=movie.synopsis,
            streaming_platforms=platforms,
            score=score,
            mood_compatibility=MoodCompatibility(
                title_valence=detail["title_valence"],
                title_arousal=detail["title_arousal"],
                distance=detail["distance"],
                fit_percentage=detail["fit_percentage"]
            ),
            match_rationale=rationale,
            front_page_description=llm_service.get_front_page_description(movie.title, movie.release_year),
            safety_check=SafetyCheckResult(
                flags_evaluated=len(movie.content_warnings),
                exclusions_passed=True,
                unknown_metadata_excluded=filter_audit["unknown_metadata_excluded_titles"]
            )
        )
        top_recommendations.append(rec)

    latency_ms = int((time.time() - start_time) * 1000)

    # Log to events table
    event = EventLog(
        session_id=request.session_id,
        mood_input=json.dumps(request.target_mood.model_dump()),
        filters_applied=json.dumps(request.filters.model_dump() if request.filters else {}),
        returned_title_ids=json.dumps([r.title_id for r in top_recommendations]),
        latency_ms=latency_ms
    )
    db.add(event)
    db.commit()

    return RecommendationResponse(
        session_id=request.session_id,
        recommendations=top_recommendations,
        meta={
            "initial_candidates": filter_audit["initial_candidates"],
            "surviving_candidates": filter_audit["surviving_candidates"],
            "dropped_reasons": filter_audit["dropped_reasons"],
            "weights_used": {"mood": weights[0], "taste": weights[1], "novelty": weights[2]},
            "latency_ms": latency_ms
        }
    )

