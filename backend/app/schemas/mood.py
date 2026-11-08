from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PickerInput(BaseModel):
    valence: float = Field(..., ge=-1.0, le=1.0, description="Pleasantness: -1.0 (unpleasant) to 1.0 (pleasant)")
    arousal: float = Field(..., ge=-1.0, le=1.0, description="Energy: -1.0 (calm/sleepy) to 1.0 (energized/tense)")

class MoodVector(BaseModel):
    valence: float
    arousal: float
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

class DistressResource(BaseModel):
    name: str
    contact: str
    url: Optional[str] = None

class DistressResponse(BaseModel):
    distress_detected: bool = True
    message: str
    helplines: List[DistressResource]
    gentle_content_option: Optional[Dict[str, Any]] = None

class MovieReference(BaseModel):
    title: str
    genres: List[str] = Field(default_factory=list)

class MoodAnalysisRequest(BaseModel):
    picker: Optional[PickerInput] = None
    free_text: Optional[str] = None
    strategy: str = Field(default="catharsis", description="'catharsis' (match mood) or 'shift' (soothe/uplift)")

class MoodAnalysisResponse(BaseModel):
    distress_detected: bool = False
    safe_response: Optional[DistressResponse] = None
    fused_mood: Optional[MoodVector] = None
    strategy_applied: Optional[str] = "catharsis"
    target_mood: Optional[MoodVector] = None
    inferred_tags: List[str] = []
    desired_genres: List[str] = Field(default_factory=list, description="Genres explicitly detected from user text")
    referenced_movies: List[MovieReference] = Field(default_factory=list, description="Referenced movies and their analyzed genres")
    source_breakdown: Dict[str, float] = {}
