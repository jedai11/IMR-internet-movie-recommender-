from typing import List, Set, Tuple, Dict, Any
from app.db.models import MovieTitle, ContentWarning
from app.schemas.recommendation import FilterCriteria

def apply_hard_filters(
    candidates: List[MovieTitle],
    filters: FilterCriteria,
    seen_title_ids: Set[str]
) -> Tuple[List[MovieTitle], Dict[str, Any]]:
    """
    Applies deterministic hard exclusion filters to candidate movie catalog.
    
    Exclusion Criteria:
    1. Seen titles (if exclude_seen is True).
    2. Runtime limits (min_runtime <= runtime <= max_runtime).
    3. Excluded genres: if candidate shares ANY excluded genre -> drop.
    4. Excluded warnings:
       - If movie has warning with status 'PRESENT' -> drop.
       - If movie has warning with status 'UNKNOWN' -> drop (UNKNOWN-metadata defense).
    5. Streaming availability: if providers specified, must match at least one.
    """
    surviving: List[MovieTitle] = []
    dropped_reasons: Dict[str, int] = {
        "seen": 0,
        "runtime": 0,
        "genre": 0,
        "origin": 0,
        "trigger_present": 0,
        "trigger_unknown": 0,
        "streaming": 0
    }
    unknown_excluded_titles: List[str] = []

    excluded_genres_lower = {g.strip().lower() for g in filters.excluded_genres if g.strip()}
    excluded_warnings_lower = {w.strip().lower() for w in filters.excluded_warnings if w.strip()}
    streaming_providers_lower = {p.strip().lower() for p in filters.streaming_providers if p.strip()}
    requested_origins_lower = {o.strip().lower() for o in filters.origins if o.strip()}
    filter_by_origin = bool(requested_origins_lower and "all" not in requested_origins_lower)

    for movie in candidates:
        # 1. Seen filter
        if filters.exclude_seen and movie.id in seen_title_ids:
            dropped_reasons["seen"] += 1
            continue

        # 2. Runtime filter
        if filters.max_runtime is not None and movie.runtime_minutes > filters.max_runtime:
            dropped_reasons["runtime"] += 1
            continue
        if filters.min_runtime is not None and movie.runtime_minutes < filters.min_runtime:
            dropped_reasons["runtime"] += 1
            continue

        # 3. Excluded Genres
        movie_genre_names = {g.name.lower() for g in movie.genres}
        if movie_genre_names.intersection(excluded_genres_lower):
            dropped_reasons["genre"] += 1
            continue

        # 4. Content / Trigger Warnings & UNKNOWN-Metadata Defense
        trigger_violation = False
        if excluded_warnings_lower:
            warning_map = {cw.warning_code.lower(): cw.status.upper() for cw in movie.content_warnings}
            
            for excluded_code in excluded_warnings_lower:
                status = warning_map.get(excluded_code)
                
                # If explicit PRESENT -> drop
                if status == "PRESENT":
                    dropped_reasons["trigger_present"] += 1
                    trigger_violation = True
                    break
                    
                # If UNKNOWN status -> strictly drop (UNKNOWN-metadata defense)
                if status == "UNKNOWN":
                    dropped_reasons["trigger_unknown"] += 1
                    unknown_excluded_titles.append(movie.title)
                    trigger_violation = True
                    break
            
            if trigger_violation:
                continue

        # 5. Streaming Availability
        if streaming_providers_lower:
            available_platforms = {av.platform.lower() for av in movie.availabilities}
            if not available_platforms.intersection(streaming_providers_lower):
                dropped_reasons["streaming"] += 1
                continue

        # 5b. Origin / Cinema Industry Filter (Hollywood, Bollywood, Tollywood, Korean, Japanese, European, etc.)
        if filter_by_origin:
            mov_origin = (getattr(movie, "origin", None) or "Hollywood").strip().lower()
            matched_origin = False
            for req in requested_origins_lower:
                if req in mov_origin:
                    matched_origin = True
                    break
                if req == "tollywood" and any(k in mov_origin for k in ("tollywood", "south", "telugu", "tamil", "malayalam", "kannada", "india")):
                    matched_origin = True
                    break
                if req == "bollywood" and any(k in mov_origin for k in ("bollywood", "hindi", "india")):
                    matched_origin = True
                    break
                if req == "hollywood" and any(k in mov_origin for k in ("hollywood", "us", "usa", "american")):
                    matched_origin = True
                    break
                if req == "korean" and any(k in mov_origin for k in ("korea", "korean", "k-drama")):
                    matched_origin = True
                    break
                if req == "japanese" and any(k in mov_origin for k in ("japan", "japanese", "anime")):
                    matched_origin = True
                    break
                if req in ("european", "intl", "asian") and any(k in mov_origin for k in ("uk", "brit", "france", "french", "german", "spain", "italy", "euro", "asia")):
                    matched_origin = True
                    break
            if not matched_origin:
                dropped_reasons["origin"] += 1
                continue

        # Survived all hard exclusion gates
        surviving.append(movie)

    # 6. Semantic Desired Genres: If user specifically requested genres in text or filters,
    # filter to candidates matching those requested genres (with graceful fallback if none match)
    preferred_genres_lower = {g.strip().lower() for g in filters.preferred_genres if g.strip()}
    if preferred_genres_lower:
        matching_preferred = [
            m for m in surviving
            if {g.name.lower() for g in m.genres}.intersection(preferred_genres_lower)
        ]
        if matching_preferred:
            surviving = matching_preferred

    audit = {
        "initial_candidates": len(candidates),
        "surviving_candidates": len(surviving),
        "dropped_reasons": dropped_reasons,
        "unknown_metadata_excluded_titles": unknown_excluded_titles[:10]
    }
    return surviving, audit

