import pytest
from app.db.models import MovieTitle, Genre, ContentWarning, Availability
from app.schemas.recommendation import FilterCriteria
from app.core.filters import apply_hard_filters

def build_mock_movie(movie_id, title, runtime, genres, warnings, platforms):
    m = MovieTitle(
        id=movie_id,
        title=title,
        release_year=2020,
        runtime_minutes=runtime,
        synopsis="Mock synopsis",
        poster_url=None,
        valence_score=0.5,
        arousal_score=0.2,
        popularity_score=8.0
    )
    m.genres = [Genre(id=i, name=g) for i, g in enumerate(genres, start=1)]
    m.content_warnings = [
        ContentWarning(id=i, title_id=movie_id, warning_code=code, status=status)
        for i, (code, status) in enumerate(warnings, start=1)
    ]
    m.availabilities = [
        Availability(id=i, title_id=movie_id, platform=p)
        for i, p in enumerate(platforms, start=1)
    ]
    return m

def test_hard_filter_runtime():
    m1 = build_mock_movie("m1", "Short Film", 80, ["Comedy"], [], ["netflix"])
    m2 = build_mock_movie("m2", "Long Epic", 180, ["Drama"], [], ["netflix"])
    
    candidates = [m1, m2]
    filters = FilterCriteria(max_runtime=100)
    surviving, audit = apply_hard_filters(candidates, filters, set())
    
    assert len(surviving) == 1
    assert surviving[0].id == "m1"
    assert audit["dropped_reasons"]["runtime"] == 1

def test_hard_filter_genre_exclusion():
    m1 = build_mock_movie("m1", "Scary Movie", 95, ["Horror", "Comedy"], [], ["netflix"])
    m2 = build_mock_movie("m2", "Fun Romcom", 95, ["Romance", "Comedy"], [], ["netflix"])
    
    candidates = [m1, m2]
    filters = FilterCriteria(excluded_genres=["Horror"])
    surviving, audit = apply_hard_filters(candidates, filters, set())
    
    assert len(surviving) == 1
    assert surviving[0].id == "m2"
    assert audit["dropped_reasons"]["genre"] == 1

def test_unknown_metadata_exclusion_defense():
    """
    CRITICAL SAFETY REQUIREMENT:
    If a user specifies a trigger exclusion (e.g. 'self_harm') and a movie has
    status 'UNKNOWN' for that trigger, the movie MUST BE STRICTLY EXCLUDED!
    """
    m_safe = build_mock_movie("m1", "Clear Title", 100, ["Drama"], [("self_harm", "ABSENT")], ["netflix"])
    m_triggered = build_mock_movie("m2", "Trigger Title", 100, ["Drama"], [("self_harm", "PRESENT")], ["netflix"])
    m_unknown = build_mock_movie("m3", "Unverified Title", 100, ["Drama"], [("self_harm", "UNKNOWN")], ["netflix"])
    
    candidates = [m_safe, m_triggered, m_unknown]
    filters = FilterCriteria(excluded_warnings=["self_harm"])
    surviving, audit = apply_hard_filters(candidates, filters, set())
    
    # Only m_safe survives! m_triggered AND m_unknown must be dropped.
    assert len(surviving) == 1
    assert surviving[0].id == "m1"
    assert audit["dropped_reasons"]["trigger_present"] == 1
    assert audit["dropped_reasons"]["trigger_unknown"] == 1
    assert "Unverified Title" in audit["unknown_metadata_excluded_titles"]

def test_seen_movies_filter():
    m1 = build_mock_movie("m1", "Movie One", 100, ["Drama"], [], ["netflix"])
    m2 = build_mock_movie("m2", "Movie Two", 100, ["Drama"], [], ["netflix"])
    
    candidates = [m1, m2]
    filters = FilterCriteria(exclude_seen=True)
    surviving, audit = apply_hard_filters(candidates, filters, seen_title_ids={"m1"})
    
    assert len(surviving) == 1
    assert surviving[0].id == "m2"
    assert audit["dropped_reasons"]["seen"] == 1

