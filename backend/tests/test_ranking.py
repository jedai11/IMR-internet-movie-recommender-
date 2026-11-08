import pytest
from app.core.ranking import calculate_mood_distance, rank_candidates
from app.core.weighting import get_recommendation_weights
from app.schemas.mood import MoodVector
from tests.test_filters import build_mock_movie

def test_mood_distance_exact_match():
    dist, fit = calculate_mood_distance(0.5, 0.5, 0.5, 0.5)
    assert dist == 0.0
    assert fit == 1.0

def test_mood_distance_opposite():
    dist, fit = calculate_mood_distance(1.0, 1.0, -1.0, -1.0)
    assert round(dist, 2) == 2.83
    assert fit == 0.0

def test_weighting_cold_start_vs_established():
    w_cold = get_recommendation_weights(interaction_count=1)
    w_established = get_recommendation_weights(interaction_count=6)
    
    assert w_cold[0] == 0.90 # 90% mood weight on cold start
    assert w_cold[1] == 0.10 # 10% taste
    
    assert w_established[0] == 0.70 # 70% mood weight on established profile
    assert w_established[1] == 0.30 # 30% taste

def test_deterministic_ranking_ordering():
    m_close = build_mock_movie("m_close", "Close Match", 100, ["Comedy"], [], ["netflix"])
    m_close.valence_score = 0.8
    m_close.arousal_score = 0.8
    
    m_far = build_mock_movie("m_far", "Far Match", 100, ["Comedy"], [], ["netflix"])
    m_far.valence_score = -0.8
    m_far.arousal_score = -0.8

    target = MoodVector(valence=0.85, arousal=0.85)
    weights = (0.9, 0.1, 0.0)

    ranked = rank_candidates([m_far, m_close], target, weights)
    
    assert len(ranked) == 2
    # m_close must be ranked first
    assert ranked[0][0].id == "m_close"
    assert ranked[0][1] > ranked[1][1]

