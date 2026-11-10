import re
from typing import List, Set, Tuple, Dict, Any
from app.db.models import MovieTitle, ContentWarning
from app.schemas.recommendation import FilterCriteria

ADULT_KEYWORDS = {
    "nudity", "nude", "sex", "sexual", "erotic", "erotica", "sensual", "explicit",
    "unrated", "nc-17", "xxx", "lust", "seduction", "steamy", "provocative", "nsfw",
    "adult", "softcore", "intercourse", "passion", "desire", "naked", "taboo"
}

def is_adult_content(movie: MovieTitle) -> bool:
    """
    Determines if a movie qualifies as 18+ adult content (nudity, sex, erotic, or mature).
    """
    if getattr(movie, "is_adult", 0) == 1:
        return True

    cert = (getattr(movie, "certification", "") or "").upper()
    if cert in ("18+", "R", "NC-17", "A", "TV-MA", "XXX", "UNRATED"):
        return True

    # Content warnings check
    warnings_present = {
        cw.warning_code.lower() for cw in getattr(movie, "content_warnings", [])
        if getattr(cw, "status", "").upper() == "PRESENT"
    }
    if any(w in warnings_present for w in ("sexual_violence", "nudity", "sex", "explicit_content")):
        return True

    # Genre check
    genre_names = {g.name.lower() for g in getattr(movie, "genres", [])}
    if any(g in genre_names for g in ("erotic", "erotica", "adult")):
        return True

    # Textual scan for sex, nudity, erotic themes
    text_corpus = f"{getattr(movie, 'title', '')} {getattr(movie, 'synopsis', '')}".lower()
    for kw in ADULT_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", text_corpus):
            return True

    return False

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

        # 5c. 18+ Adult Content Filter (Nudity, Sex, Erotic, Explicit Cinema)
        # adult_mode: "standard" (family/PG-13 only), "include_18" / "all" (all ratings), "18_plus" (18+ mature only)
        adult_mode = (getattr(filters, "adult_mode", None) or "all").lower()
        is_adult_movie = is_adult_content(movie)

        if adult_mode == "18_plus" and not is_adult_movie:
            dropped_reasons["adult_maturity"] = dropped_reasons.get("adult_maturity", 0) + 1
            continue
        elif adult_mode == "standard" and is_adult_movie:
            dropped_reasons["adult_maturity"] = dropped_reasons.get("adult_maturity", 0) + 1
            continue

        # 5d. Censorship Filter ('all', 'censored', 'uncensored')
        censorship_mode = (getattr(filters, "censorship", None) or "all").lower()
        movie_censorship = (getattr(movie, "censorship", "") or "censored").lower()
        if censorship_mode == "uncensored":
            if movie_censorship != "uncensored" and not is_adult_movie:
                dropped_reasons["censorship"] = dropped_reasons.get("censorship", 0) + 1
                continue
        elif censorship_mode == "censored":
            if movie_censorship == "uncensored":
                dropped_reasons["censorship"] = dropped_reasons.get("censorship", 0) + 1
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

