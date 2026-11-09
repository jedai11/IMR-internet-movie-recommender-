import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import engine, Base, SessionLocal
from app.db.seed_data import seed_database

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()
    yield

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_mood_analyze_picker_only(client):
    payload = {
        "picker": {"valence": 0.6, "arousal": 0.4},
        "strategy": "catharsis"
    }
    response = client.post("/api/mood/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["distress_detected"] is False
    assert data["fused_mood"]["valence"] == 0.6
    assert data["fused_mood"]["arousal"] == 0.4
    assert data["source_breakdown"]["picker"] == 1.0

def test_mood_analyze_distress_trigger(client):
    payload = {
        "free_text": "I can't go on anymore and want to kill myself",
        "strategy": "shift"
    }
    response = client.post("/api/mood/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["distress_detected"] is True
    assert data["safe_response"] is not None
    assert len(data["safe_response"]["helplines"]) >= 2
    assert "988" in data["safe_response"]["helplines"][0]["contact"]

def test_recommendation_pipeline_end_to_end(client):
    payload = {
        "session_id": "test_session_123",
        "target_mood": {"valence": 0.8, "arousal": 0.5, "confidence": 1.0},
        "strategy": "catharsis",
        "filters": {
            "max_runtime": 130,
            "excluded_genres": ["Horror"],
            "excluded_warnings": ["self_harm"]
        },
        "limit": 3
    }
    response = client.post("/api/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test_session_123"
    assert len(data["recommendations"]) <= 3
    for rec in data["recommendations"]:
        assert rec["runtime_minutes"] <= 130
        assert "Horror" not in rec["genres"]
        assert rec["match_rationale"] is not None
        assert rec["mood_compatibility"]["fit_percentage"] > 0

def test_recommendation_with_bollywood_origin_filter(client):
    payload = {
        "session_id": "test_session_bolly",
        "mood_name": "joyful",
        "filters": {
            "origins": ["bollywood"]
        },
        "limit": 5
    }
    response = client.post("/api/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["recommendations"]) > 0
    assert "origin_keys" in data["meta"]
    assert "bollywood" in data["meta"]["origin_keys"]
    for rec in data["recommendations"]:
        assert rec["origin"] == "Bollywood"
        assert rec["tmdb_id"] is not None

def test_feedback_submission(client):
    payload = {
        "session_id": "test_session_123",
        "title_id": "m_q1_01", # Amelie
        "feedback_action": "helped"
    }
    response = client.post("/api/feedback", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_semantic_genre_detection_in_text(client):
    payload = {
        "free_text": "I had an exhausting week and I want to watch an intense thriller",
        "strategy": "catharsis"
    }
    response = client.post("/api/mood/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Thriller" in data["desired_genres"]
    assert "exhausting" in data["inferred_tags"]

def test_movie_reference_and_genre_analysis(client):
    payload = {
        "free_text": "I really loved Parasite and Train to Busan, recommend me something similar",
        "strategy": "catharsis"
    }
    response = client.post("/api/mood/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Thriller" in data["desired_genres"]
    assert "Action" in data["desired_genres"] or "Drama" in data["desired_genres"]
    ref_titles = [r["title"] for r in data["referenced_movies"]]
    assert any("Parasite" in t for t in ref_titles)
