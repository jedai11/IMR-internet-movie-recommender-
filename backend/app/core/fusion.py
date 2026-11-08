import math
from typing import Optional, Tuple, Dict
from app.schemas.mood import PickerInput, MoodVector

def fuse_mood_modalities(
    picker: Optional[PickerInput],
    text_vector: Optional[MoodVector]
) -> Tuple[MoodVector, Dict[str, float]]:
    """
    Fuses explicit 2D picker input and NLP text extraction.
    Explicit picker has base confidence 1.0.
    NLP text extraction has variable confidence (typically 0.40 - 0.90).
    """
    if picker is None and text_vector is None:
        # Default neutral calm if nothing provided
        return MoodVector(valence=0.0, arousal=0.0, confidence=0.5), {"picker": 0.0, "text": 0.0}

    if picker is not None and text_vector is None:
        return MoodVector(valence=picker.valence, arousal=picker.arousal, confidence=1.0), {"picker": 1.0, "text": 0.0}

    if picker is None and text_vector is not None:
        return MoodVector(valence=text_vector.valence, arousal=text_vector.arousal, confidence=text_vector.confidence), {"picker": 0.0, "text": 1.0}

    # Both are present -> Confidence-weighted fusion
    w_picker = 1.0
    w_text = max(0.1, min(1.0, text_vector.confidence))

    total_w = w_picker + w_text
    norm_w_picker = w_picker / total_w
    norm_w_text = w_text / total_w

    fused_valence = (picker.valence * norm_w_picker) + (text_vector.valence * norm_w_text)
    fused_arousal = (picker.arousal * norm_w_picker) + (text_vector.arousal * norm_w_text)

    # Clamping
    fused_valence = max(-1.0, min(1.0, fused_valence))
    fused_arousal = max(-1.0, min(1.0, fused_arousal))

    # Fused confidence combining both independent signals
    combined_conf = min(1.0, math.sqrt(w_picker**2 + w_text**2) / math.sqrt(2.0))

    return (
        MoodVector(
            valence=round(fused_valence, 3),
            arousal=round(fused_arousal, 3),
            confidence=round(combined_conf, 3)
        ),
        {
            "picker": round(norm_w_picker, 3),
            "text": round(norm_w_text, 3)
        }
    )

