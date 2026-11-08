import math
from typing import List, Tuple, Dict, Any, Set
from app.db.models import MovieTitle
from app.schemas.mood import MoodVector

MAX_CIRCUMPLEX_DISTANCE = math.sqrt(2.0**2 + 2.0**2) # sqrt(8) ~ 2.828427

def calculate_mood_distance(v1: float, a1: float, v2: float, a2: float) -> Tuple[float, float]:
    """
    Returns (euclidean_distance, normalized_fit_score [0.0, 1.0])
    """
    dist = math.sqrt((v1 - v2)**2 + (a1 - a2)**2)
    fit = max(0.0, 1.0 - (dist / MAX_CIRCUMPLEX_DISTANCE))
    return round(dist, 4), round(fit, 4)

def rank_candidates(
    candidates: List[MovieTitle],
    target_mood: MoodVector,
    weights: Tuple[float, float, float], # (w_mood, w_taste, w_novelty)
    liked_genre_names: Set[str] = set(),
    disliked_genre_names: Set[str] = set(),
    preferred_genre_names: Set[str] = set() # Semantically requested genres (e.g., Thriller, Comedy)
) -> List[Tuple[MovieTitle, float, Dict[str, Any]]]:
    """
    Deterministic scoring and ranking algorithm.
    Score = w_mood * MoodFit + w_taste * TasteFit + w_novelty * Novelty (+ Semantic Genre Match Priority)
    """
    w_mood, w_taste, w_novelty = weights
    scored_candidates = []
    preferred_lower = {g.lower() for g in preferred_genre_names if g}

    for movie in candidates:
        dist, mood_fit = calculate_mood_distance(
            movie.valence_score,
            movie.arousal_score,
            target_mood.valence,
            target_mood.arousal
        )

        # Base TasteFit calculation (0.0 to 1.0)
        # 1. Normalized popularity baseline
        taste_fit = min(1.0, max(0.1, movie.popularity_score / 10.0))
        
        # 2. Genre preference adjustments
        movie_genre_names = {g.name.lower() for g in movie.genres}
        if liked_genre_names and movie_genre_names.intersection(liked_genre_names):
            taste_fit = min(1.0, taste_fit + 0.15)
        if disliked_genre_names and movie_genre_names.intersection(disliked_genre_names):
            taste_fit = max(0.0, taste_fit - 0.25)

        # 3. Semantic Genre Matching: Check if movie matches user's specifically requested genres
        matched_preferred = []
        genre_match_boost = 0.0
        if preferred_lower:
            overlap = movie_genre_names.intersection(preferred_lower)
            if overlap:
                matched_preferred = [g.name for g in movie.genres if g.name.lower() in overlap]
                # High priority boost ensures requested genre candidates rank above non-matching genres,
                # with compounding weight when matching multiple requested semantic dimensions (e.g., Night-Movie + Romance + Thriller)
                genre_match_boost = 2.0 * len(overlap)

        # Composite score
        total_score = (w_mood * mood_fit) + (w_taste * taste_fit) + genre_match_boost
        
        detail = {
            "title_valence": movie.valence_score,
            "title_arousal": movie.arousal_score,
            "distance": dist,
            "mood_fit": mood_fit,
            "taste_fit": taste_fit,
            "fit_percentage": int(round(mood_fit * 100)),
            "matched_preferred_genre": matched_preferred[0] if matched_preferred else None
        }

        scored_candidates.append((movie, round(total_score, 4), detail))

    # Sort descending by score, tie-break on popularity and id
    scored_candidates.sort(key=lambda item: (item[1], item[0].popularity_score, item[0].id), reverse=True)
    return scored_candidates

