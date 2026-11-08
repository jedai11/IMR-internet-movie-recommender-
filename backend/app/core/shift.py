from app.schemas.mood import MoodVector
from app.core.config import settings

def calculate_target_mood(current_mood: MoodVector, strategy: str = "catharsis") -> MoodVector:
    """
    Computes target recommendation vector based on user strategy.
    - Catharsis: Match user where they are (validate current emotion).
    - Shift: Apply emotional regulation trajectory towards positive valence and balanced arousal.
    """
    if strategy.lower() != "shift":
        return MoodVector(
            valence=current_mood.valence,
            arousal=current_mood.arousal,
            confidence=current_mood.confidence
        )

    # Shift mode:
    # Ideal gentle recovery point in Russell's circumplex:
    # Warm positive valence (+0.55), calm/comforting slightly low arousal (-0.10)
    ideal_valence = 0.55
    ideal_arousal = -0.10

    # Step size
    step = settings.SHIFT_STEP_FACTOR

    # Interpolate towards ideal
    target_v = current_mood.valence + step * (ideal_valence - current_mood.valence)
    target_a = current_mood.arousal + step * (ideal_arousal - current_mood.arousal)

    # Clamping
    target_v = max(-1.0, min(1.0, target_v))
    target_a = max(-1.0, min(1.0, target_a))

    return MoodVector(
        valence=round(target_v, 3),
        arousal=round(target_a, 3),
        confidence=current_mood.confidence
    )

