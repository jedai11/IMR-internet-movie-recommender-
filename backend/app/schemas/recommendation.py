from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.schemas.mood import MoodVector

class FilterCriteria(BaseModel):
    max_runtime: Optional[int] = Field(default=None, ge=30, le=360)
    min_runtime: Optional[int] = Field(default=None, ge=30, le=360)
    excluded_genres: List[str] = Field(default_factory=list)
    preferred_genres: List[str] = Field(default_factory=list, description="Preferred genres extracted semantically or explicitly selected")
    origins: List[str] = Field(default_factory=list, description="Origins or cinema industries requested: hollywood, bollywood, tollywood, korean, japanese, etc.")
    adult_mode: Optional[str] = Field(default="all", description="Maturity setting: 'standard' (family/PG-13 only), 'all' (all ratings), or '18_plus' (mature/adult only)")
    censorship: Optional[str] = Field(default="all", description="Censorship setting: 'all', 'censored' (theatrical/clean edits), or 'uncensored' (raw/director's cut)")
    # trigger codes: 'self_harm', 'sexual_violence', 'substance_abuse', 'grief_loss', 'panic_attacks', 'violence'
    excluded_warnings: List[str] = Field(default_factory=list)
    streaming_providers: List[str] = Field(default_factory=list) # e.g. ['netflix', 'prime', 'free']
    exclude_seen: bool = True

class RecommendationRequest(BaseModel):
    session_id: str
    target_mood: Optional[MoodVector] = None
    mood_name: Optional[str] = None
    strategy: str = Field(default="catharsis")
    filters: Optional[FilterCriteria] = Field(default_factory=FilterCriteria)
    limit: int = Field(default=36, ge=1, le=100)

class MoodCompatibility(BaseModel):
    title_valence: float = 0.0
    title_arousal: float = 0.0
    distance: float = 0.0
    fit_percentage: int = 100

class SafetyCheckResult(BaseModel):
    flags_evaluated: int = 0
    exclusions_passed: bool = True
    unknown_metadata_excluded: List[str] = []

class MovieRecommendation(BaseModel):
    title_id: str
    tmdb_id: Optional[int] = None
    title: str
    release_year: Optional[int] = None
    runtime_minutes: Optional[int] = 0
    genres: List[str] = Field(default_factory=list)
    origin: Optional[str] = Field(default="TMDB", description="Origin/Cinema industry")
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    tmdb_url: Optional[str] = None
    synopsis: Optional[str] = None
    streaming_platforms: List[str] = Field(default_factory=list)
    score: float = 1.0
    mood_compatibility: Optional[MoodCompatibility] = None
    match_rationale: Optional[str] = None
    front_page_description: Optional[str] = Field(default=None, description="Official theatrical front-page poster description verified by Gemini")
    safety_check: Optional[SafetyCheckResult] = None
    tmdb_rating: Optional[float] = Field(default=None, description="Official TMDB user rating out of 10")
    vote_count: Optional[int] = Field(default=None, description="TMDB vote count")
    trailer_url: Optional[str] = Field(default=None, description="Official YouTube trailer URL")
    is_adult: Optional[bool] = Field(default=False, description="Whether title is an 18+ mature film")
    censorship: Optional[str] = Field(default="censored", description="Censorship version: 'censored' or 'uncensored'")
    certification: Optional[str] = Field(default=None, description="Film certification (e.g., '18+', 'R', 'PG-13', 'A')")

class RecommendationResponse(BaseModel):
    session_id: str
    recommendations: List[MovieRecommendation]
    meta: Dict[str, Any]

