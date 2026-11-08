from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.schemas.mood import MoodVector

class FilterCriteria(BaseModel):
    max_runtime: Optional[int] = Field(default=None, ge=30, le=360)
    min_runtime: Optional[int] = Field(default=None, ge=30, le=360)
    excluded_genres: List[str] = Field(default_factory=list)
    preferred_genres: List[str] = Field(default_factory=list, description="Preferred genres extracted semantically or explicitly selected")
    # trigger codes: 'self_harm', 'sexual_violence', 'substance_abuse', 'grief_loss', 'panic_attacks', 'violence'
    excluded_warnings: List[str] = Field(default_factory=list)
    streaming_providers: List[str] = Field(default_factory=list) # e.g. ['netflix', 'prime', 'free']
    exclude_seen: bool = True

class RecommendationRequest(BaseModel):
    session_id: str
    target_mood: MoodVector
    strategy: str = Field(default="catharsis")
    filters: Optional[FilterCriteria] = Field(default_factory=FilterCriteria)
    limit: int = Field(default=5, ge=1, le=20)

class MoodCompatibility(BaseModel):
    title_valence: float
    title_arousal: float
    distance: float
    fit_percentage: int

class SafetyCheckResult(BaseModel):
    flags_evaluated: int
    exclusions_passed: bool
    unknown_metadata_excluded: List[str] = []

class MovieRecommendation(BaseModel):
    title_id: str
    title: str
    release_year: int
    runtime_minutes: int
    genres: List[str]
    poster_url: Optional[str] = None
    synopsis: Optional[str] = None
    streaming_platforms: List[str]
    score: float
    mood_compatibility: MoodCompatibility
    match_rationale: str
    front_page_description: Optional[str] = Field(default=None, description="Official theatrical front-page poster description verified by Gemini")
    safety_check: SafetyCheckResult

class RecommendationResponse(BaseModel):
    session_id: str
    recommendations: List[MovieRecommendation]
    meta: Dict[str, Any]

