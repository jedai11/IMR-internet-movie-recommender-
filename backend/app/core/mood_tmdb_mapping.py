"""
MOOD -> TMDB DISCOVER QUERY MAPPING CONFIGURATION

You can edit this mapping to customize which TMDB genres, sort orders, and filters
are triggered for each human emotional state.

TMDB Genre ID Reference:
  Action: 28        | Adventure: 12      | Animation: 16       | Comedy: 35
  Crime: 80         | Documentary: 99    | Drama: 18           | Family: 10751
  Fantasy: 14       | History: 36        | Horror: 27          | Music: 10402
  Mystery: 9648     | Romance: 10749     | Science Fiction: 878| TV Movie: 10770
  Thriller: 53      | War: 10752         | Western: 37
"""

import re
from typing import Dict, Any, Optional, List

# Configurable cache expiry (default 7 days)
DEFAULT_CACHE_EXPIRY_DAYS = 7

# TMDB HTTP Request Constraints
TMDB_TIMEOUT_SECONDS = 6.0
TMDB_MAX_RETRIES = 2

# Origin / Cinema Industry to TMDB ISO Language Code Mapping
ORIGIN_LANGUAGE_MAP: Dict[str, str] = {
    "bollywood": "hi",
    "tollywood": "te|ta|ml|kn",
    "korean": "ko",
    "japanese": "ja",
    "hollywood": "en",
    "european": "en|fr|de|es|it",
    "french": "fr",
    "spanish": "es",
    "german": "de",
    "italian": "it",
    "asian": "hi|te|ta|ml|kn|ko|ja|zh|th"
}

ORIGIN_SYNONYMS: Dict[str, str] = {
    # Bollywood / Hindi
    "bollywood": "bollywood",
    "bolly": "bollywood",
    "hindi": "bollywood",
    "indian": "bollywood",
    "india": "bollywood",
    # Tollywood / South Indian
    "tollywood": "tollywood",
    "tolly": "tollywood",
    "telugu": "tollywood",
    "tamil": "tollywood",
    "malayalam": "tollywood",
    "kannada": "tollywood",
    "south indian": "tollywood",
    "south": "tollywood",
    # Korean
    "korean": "korean",
    "korea": "korean",
    "kdrama": "korean",
    "k-drama": "korean",
    # Japanese
    "japanese": "japanese",
    "japan": "japanese",
    "anime": "japanese",
    # Hollywood / English
    "hollywood": "hollywood",
    "american": "hollywood",
    "english": "hollywood",
    "us": "hollywood",
    # European
    "european": "european",
    "europe": "european",
    "french": "french",
    "france": "french",
    "german": "german",
    "germany": "german",
    "spanish": "spanish",
    "spain": "spanish",
    "italian": "italian",
    "italy": "italian",
    "british": "hollywood",
    "uk": "hollywood",
    # Asian / International
    "asian": "asian",
    "asia": "asian",
    "chinese": "asian",
    "china": "asian"
}

# Mood -> TMDB Query Parameter Mapping
# Edit the parameters below to tune movie discovery per mood:
MOOD_TMDB_MAPPING: Dict[str, Dict[str, Any]] = {
    "angry": {
        "name": "Angry & Agitated",
        "description": "High-octane, gripping action, crime, and relentless thrillers to channel intensity",
        "with_genres": "28|80|53",       # Action OR Crime OR Thriller
        "without_genres": "10749,10751", # Exclude Romance, Family
        "sort_by": "popularity.desc",
        "vote_count_gte": 100
    },
    "sad": {
        "name": "Sad & Melancholic",
        "description": "Deeply reflective, poignant dramas and emotional storytelling for cathartic release",
        "with_genres": "18|10402",       # Drama OR Music
        "without_genres": "27",          # Exclude Horror
        "sort_by": "popularity.desc",
        "vote_count_gte": 100
    },
    "calm": {
        "name": "Calm & Peaceful",
        "description": "Gentle, aesthetically serene, heartwarming animation and comforting cinema",
        "with_genres": "16|10751|99",    # Animation OR Family OR Documentary
        "without_genres": "27,53,80",    # Exclude Horror, Thriller, Crime
        "sort_by": "popularity.desc",
        "vote_count_gte": 80
    },
    "joyful": {
        "name": "Joyful & Energetic",
        "description": "Uplifting comedies, vibrant adventures, and pure feel-good cinema",
        "with_genres": "35|12|16",       # Comedy OR Adventure OR Animation
        "without_genres": "27,18",       # Exclude Horror, Heavy Drama
        "sort_by": "popularity.desc",
        "vote_count_gte": 100
    },
    "romantic": {
        "name": "Romantic & Tender",
        "description": "Intimate love stories, tender romances, and heartfelt relationship dramas",
        "with_genres": "10749|18",       # Romance OR Drama
        "without_genres": "27,80",       # Exclude Horror, Crime
        "sort_by": "popularity.desc",
        "vote_count_gte": 80
    },
    "stressed": {
        "name": "Stressed & Anxious",
        "description": "Escapist fantasies, lighthearted comedy, and reassuring worlds to decompress",
        "with_genres": "35|14|10751",    # Comedy OR Fantasy OR Family
        "without_genres": "27,53,80",    # Strictly drop Horror, Thriller, Crime
        "sort_by": "popularity.desc",
        "vote_count_gte": 100
    },
    "bored": {
        "name": "Bored & Restless",
        "description": "Mind-bending sci-fi, unpredictable mysteries, and high-intrigue thrillers to spark curiosity",
        "with_genres": "878|9648|53",    # Sci-Fi OR Mystery OR Thriller
        "without_genres": "",
        "sort_by": "popularity.desc",
        "vote_count_gte": 100
    },
    "focus": {
        "name": "Focus & Contemplative",
        "description": "Disciplined masterworks, historical epics, and intellectually stimulating narratives",
        "with_genres": "18|36|9648",     # Drama OR History OR Mystery
        "without_genres": "27",          # Exclude Horror
        "sort_by": "popularity.desc",
        "vote_count_gte": 150
    },
    "fearful": {
        "name": "Fearful / Horror Thrill",
        "description": "Spine-chilling supernatural horror and dark psychological mysteries",
        "with_genres": "27|9648",        # Horror OR Mystery
        "without_genres": "10751",       # Exclude Family
        "sort_by": "popularity.desc",
        "vote_count_gte": 100
    },
    "default": {
        "name": "Universal Discovery",
        "description": "Acclaimed global cinema balanced across emotional spectrums",
        "with_genres": "18|35|12",       # Drama OR Comedy OR Adventure
        "without_genres": "",
        "sort_by": "popularity.desc",
        "vote_count_gte": 100
    }
}

# Synonyms and keyword mapping to canonical mood keys
MOOD_SYNONYMS: Dict[str, str] = {
    # Angry
    "angry": "angry", "mad": "angry", "furious": "angry", "agitated": "angry", "rage": "angry",
    # Sad
    "sad": "sad", "depressed": "sad", "melancholy": "sad", "melancholic": "sad", "grief": "sad",
    "unhappy": "sad", "crying": "sad", "lonely": "sad", "heartbroken": "sad", "gloomy": "sad",
    # Calm
    "calm": "calm", "peaceful": "calm", "relaxed": "calm", "cozy": "calm", "serene": "calm",
    "chill": "calm", "tranquil": "calm", "soothing": "calm", "zen": "calm",
    # Joyful
    "joyful": "joyful", "happy": "joyful", "excited": "joyful", "energetic": "joyful",
    "cheerful": "joyful", "thrilled": "joyful", "upbeat": "joyful", "fun": "joyful",
    # Romantic
    "romantic": "romantic", "romance": "romantic", "love": "romantic", "intimate": "romantic",
    "tender": "romantic", "passion": "romantic", "flirty": "romantic",
    # Stressed
    "stressed": "stressed", "anxious": "stressed", "overwhelmed": "stressed", "tense": "stressed",
    "nervous": "stressed", "panic": "stressed", "frustrated": "stressed",
    # Bored
    "bored": "bored", "restless": "bored", "lethargic": "bored", "uninspired": "bored", "curious": "bored",
    # Focus
    "focus": "focus", "contemplative": "focus", "deep": "focus", "thoughtful": "focus",
    "intellectual": "focus", "disciplined": "focus",
    # Fearful / Horror
    "horror": "fearful", "scared": "fearful", "creepy": "fearful", "spooky": "fearful", "fear": "fearful"
}

def resolve_mood_key(
    mood_name: Optional[str] = None,
    text: Optional[str] = None,
    valence: Optional[float] = None,
    arousal: Optional[float] = None
) -> str:
    """
    Resolves input text, mood preset name, or (valence, arousal) affect coordinates
    to a canonical mood key defined in MOOD_TMDB_MAPPING.
    """
    # 1. Direct mood name check
    if mood_name:
        clean = mood_name.strip().lower()
        if clean in MOOD_TMDB_MAPPING:
            return clean
        if clean in MOOD_SYNONYMS:
            return MOOD_SYNONYMS[clean]

    # 2. Text keyword scan
    if text:
        lower = text.lower()
        for token, canonical in MOOD_SYNONYMS.items():
            if token in lower:
                return canonical

    # 3. Russell's Circumplex Affect Coordinates fallback
    if valence is not None and arousal is not None:
        if valence >= 0.3 and arousal >= 0.2:
            return "joyful"
        elif valence >= 0.3 and arousal < 0.2:
            return "calm"
        elif valence <= -0.2 and arousal > 0.2:
            return "angry"
        elif valence <= -0.2 and arousal <= 0.0:
            return "sad"
        elif valence < 0.2 and arousal > 0.3:
            return "stressed"
        elif valence < 0.2 and arousal < -0.3:
            return "bored"
        elif abs(valence) < 0.3:
            return "focus"

    return "default"

def resolve_origin_keys(origins: Optional[List[str]] = None, text: Optional[str] = None) -> List[str]:
    """
    Normalizes requested origin codes from filters or free-text into canonical origin keys.
    Returns list of canonical origin keys (e.g. ['bollywood'] or ['korean']).
    If empty or 'all', returns empty list (all world cinema).
    """
    canonical_origins = set()
    if origins:
        for o in origins:
            clean = o.strip().lower()
            if clean == "all":
                return []
            if clean in ORIGIN_LANGUAGE_MAP:
                canonical_origins.add(clean)
            elif clean in ORIGIN_SYNONYMS:
                canonical_origins.add(ORIGIN_SYNONYMS[clean])

    # Also detect origin keywords from query text if origins list was not explicitly set
    if not canonical_origins and text:
        lower = text.lower()
        for token, canon in ORIGIN_SYNONYMS.items():
            pattern = r"\b" + re.escape(token) + r"\b"
            if re.search(pattern, lower):
                canonical_origins.add(canon)

    return sorted(list(canonical_origins))

def get_origin_language_param(origin_keys: List[str]) -> Optional[str]:
    """
    Combines ISO 639-1 language codes for TMDB's with_original_language parameter
    using TMDB's pipe-OR syntax.
    """
    langs = []
    for ok in origin_keys:
        lang_code = ORIGIN_LANGUAGE_MAP.get(ok)
        if lang_code:
            langs.append(lang_code)
    return "|".join(langs) if langs else None

def get_tmdb_query_params(
    mood_key: str,
    page: int = 1,
    origin_keys: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Returns query parameters for TMDB's /discover/movie endpoint based on the mood key
    and optional cinema origin keys (e.g. ['bollywood'], ['korean']).
    """
    config = MOOD_TMDB_MAPPING.get(mood_key, MOOD_TMDB_MAPPING["default"])
    params: Dict[str, Any] = {
        "page": page,
        "include_adult": "false",
        "include_video": "false"
    }

    if config.get("with_genres"):
        params["with_genres"] = config["with_genres"]
    if config.get("without_genres"):
        params["without_genres"] = config["without_genres"]
    if config.get("sort_by"):
        params["sort_by"] = config["sort_by"]
    if config.get("vote_count_gte"):
        params["vote_count.gte"] = config["vote_count_gte"]
    if config.get("vote_average_gte"):
        params["vote_average.gte"] = config["vote_average_gte"]

    # Apply origin / cinema language constraints if requested
    if origin_keys:
        lang_param = get_origin_language_param(origin_keys)
        if lang_param:
            params["with_original_language"] = lang_param
            # For non-Hollywood origins, TMDB global vote counts are naturally lower.
            # Relax vote_count threshold so international cinema isn't filtered out.
            has_non_hollywood = any(ok != "hollywood" for ok in origin_keys)
            if has_non_hollywood:
                params["vote_count.gte"] = 10
                # Stressed mood excludes crime (80), which eliminates many Hindi family dramas;
                # relax to only exclude horror and thriller
                if mood_key == "stressed":
                    params["without_genres"] = "27,53"

    return params

