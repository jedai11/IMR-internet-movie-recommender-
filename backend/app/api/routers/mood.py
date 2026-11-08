from fastapi import APIRouter
from app.schemas.mood import MoodAnalysisRequest, MoodAnalysisResponse
from app.core.distress import distress_safeguard
from app.core.fusion import fuse_mood_modalities
from app.core.shift import calculate_target_mood
from app.core.llm_service import llm_service

router = APIRouter(prefix="/mood", tags=["mood"])

@router.post("/analyze", response_model=MoodAnalysisResponse)
def analyze_mood(request: MoodAnalysisRequest):
    """
    Analyzes multimodal mood input (2D picker + free-text).
    1. Evaluates distress safeguard on free-text (short-circuits if crisis detected).
    2. Extracts structured valence/arousal, desired genres, and referenced movie analysis from text.
    3. Fuses picker and text modalities using confidence-weighting.
    4. Computes target mood trajectory based on strategy (catharsis vs. shift).
    """
    # 1. Distress Safeguard
    distress_found, distress_payload = distress_safeguard.evaluate(request.free_text)
    if distress_found:
        return MoodAnalysisResponse(
            distress_detected=True,
            safe_response=distress_payload,
            fused_mood=None,
            strategy_applied=request.strategy,
            target_mood=None,
            inferred_tags=["distress_interception"],
            source_breakdown={"distress_override": 1.0}
        )

    # 2. Text NLP & Movie Reference Extraction (if text provided)
    text_vector = None
    inferred_tags = []
    desired_genres = []
    referenced_movies = []
    if request.free_text and request.free_text.strip():
        text_vector, inferred_tags, desired_genres, referenced_movies = llm_service.extract_mood(request.free_text.strip())

    # 3. Multimodal Fusion
    fused_vector, source_breakdown = fuse_mood_modalities(
        picker=request.picker,
        text_vector=text_vector
    )

    # 4. Strategy & Target Trajectory Calculation
    target_vector = calculate_target_mood(fused_vector, strategy=request.strategy)

    return MoodAnalysisResponse(
        distress_detected=False,
        safe_response=None,
        fused_mood=fused_vector,
        strategy_applied=request.strategy,
        target_mood=target_vector,
        inferred_tags=inferred_tags,
        desired_genres=desired_genres,
        referenced_movies=referenced_movies,
        source_breakdown=source_breakdown
    )
