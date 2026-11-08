from typing import Tuple
from app.core.config import settings

def get_recommendation_weights(interaction_count: int = 0) -> Tuple[float, float, float]:
    """
    Computes (w_mood, w_taste, w_novelty) dynamically based on user profile maturity.
    - Cold-start users rely heavily (90%) on explicit mood signal.
    - Established users balance current mood with historical taste affinity (70% mood / 30% taste).
    """
    if interaction_count <= settings.COLD_START_THRESHOLD:
        return (
            settings.COLD_START_W_MOOD,
            settings.COLD_START_W_TASTE,
            settings.DEFAULT_W_NOVELTY
        )
    else:
        return (
            settings.ESTABLISHED_W_MOOD,
            settings.ESTABLISHED_W_TASTE,
            settings.DEFAULT_W_NOVELTY
        )

