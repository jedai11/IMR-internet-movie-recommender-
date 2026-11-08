import pytest
from app.core.distress import distress_safeguard

CRISIS_PHRASES = [
    "I want to kill myself",
    "I feel like ending my life tonight",
    "there is no reason to live anymore",
    "I'm thinking about suicide",
    "better off dead than feeling this way",
    "I can't go on anymore please help",
    "thinking of cutting myself",
    "i just wanna die",
    "gonna overdose on pills",
    "don't want to wake up ever again"
]

BENIGN_PHRASES = [
    "I had a really tiring day at the office and just want to sleep",
    "Feeling a bit sad after breaking up, want a good comforting film",
    "Looking for a thrilling horror movie with high adrenaline",
    "In a cheerful mood ready to celebrate with friends",
    "Feeling melancholic and reflective, maybe an indie drama",
    "My feet are killing me after running a marathon",
    "I'm dying of laughter from that stand-up routine",
    "Super stressed about my exam tomorrow, need a break",
    "Feeling anxious about job interview but staying hopeful",
    "Want something calm and peaceful before bed"
]

def test_distress_detected_on_crisis_phrases():
    for phrase in CRISIS_PHRASES:
        detected, payload = distress_safeguard.evaluate(phrase)
        assert detected is True, f"Failed to detect crisis in: '{phrase}'"
        assert payload is not None
        assert payload.distress_detected is True
        assert len(payload.helplines) >= 2
        assert "988" in payload.helplines[0].contact or "741741" in payload.helplines[1].contact

def test_distress_not_detected_on_benign_phrases():
    for phrase in BENIGN_PHRASES:
        detected, payload = distress_safeguard.evaluate(phrase)
        assert detected is False, f"False positive crisis detection on: '{phrase}'"
        assert payload is None

