from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

def utc_now():
    return datetime.now(timezone.utc)

# Many-to-many link between MovieTitle and Genre
title_genres_table = Table(
    "title_genres",
    Base.metadata,
    Column("title_id", String, ForeignKey("titles.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True)
)

class MovieTitle(Base):
    __tablename__ = "titles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    release_year = Column(Integer, nullable=False)
    runtime_minutes = Column(Integer, nullable=False)
    synopsis = Column(Text, nullable=True)
    poster_url = Column(String, nullable=True)
    
    # Emotional Affective Coordinates (Russell Circumplex)
    valence_score = Column(Float, nullable=False, default=0.0)
    arousal_score = Column(Float, nullable=False, default=0.0)
    valence_arousal_source = Column(String, default="editorial_estimate")
    valence_arousal_confidence = Column(Float, default=0.90)
    ending_tone = Column(String, default="uplifting")
    popularity_score = Column(Float, default=7.5)
    origin = Column(String, default="Hollywood", index=True)

    # Relationships
    genres = relationship("Genre", secondary=title_genres_table, back_populates="titles")
    content_warnings = relationship("ContentWarning", back_populates="title", cascade="all, delete-orphan")
    availabilities = relationship("Availability", back_populates="title", cascade="all, delete-orphan")
    ratings = relationship("UserRating", back_populates="title")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    
    titles = relationship("MovieTitle", secondary=title_genres_table, back_populates="genres")

class ContentWarning(Base):
    __tablename__ = "content_warnings"

    id = Column(Integer, primary_key=True, index=True)
    title_id = Column(String, ForeignKey("titles.id"), nullable=False, index=True)
    warning_code = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, default="ABSENT")
    confidence = Column(Float, default=1.0)
    source = Column(String, default="editorial_curated")

    title = relationship("MovieTitle", back_populates="content_warnings")

class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)
    title_id = Column(String, ForeignKey("titles.id"), nullable=False, index=True)
    platform = Column(String, nullable=False, index=True)
    region = Column(String, default="GLOBAL")

    title = relationship("MovieTitle", back_populates="availabilities")

class UserRating(Base):
    __tablename__ = "user_ratings"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False, index=True)
    title_id = Column(String, ForeignKey("titles.id"), nullable=False)
    feedback_action = Column(String, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    title = relationship("MovieTitle", back_populates="ratings")

class EventLog(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False, index=True)
    mood_input = Column(Text, nullable=True)
    filters_applied = Column(Text, nullable=True)
    returned_title_ids = Column(Text, nullable=True)
    latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)

class TMDBMovieQueue(Base):
    """
    FIFO Queue table for raw movies abstracted from TMDB awaiting ingestion.
    Ensures structured, deduplicated queuing before catalog promotion.
    """
    __tablename__ = "tmdb_movie_queue"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tmdb_id = Column(Integer, index=True, nullable=False)
    title = Column(String, nullable=False)
    genre_name = Column(String, nullable=False, index=True)
    status = Column(String, default="QUEUED", index=True)  # QUEUED, PROCESSED, SKIPPED
    payload_json = Column(Text, nullable=True)
    queued_at = Column(DateTime, default=utc_now)
    processed_at = Column(DateTime, nullable=True)

class TMDBMovieStack(Base):
    """
    LIFO Stack table for active and historical recommended movie sequences.
    Enables instant LIFO peek/pop retrieval for genres without repeat TMDB queries.
    """
    __tablename__ = "tmdb_movie_stack"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, index=True, nullable=True)
    title_id = Column(String, ForeignKey("titles.id"), nullable=False, index=True)
    tmdb_id = Column(Integer, nullable=True)
    genre_name = Column(String, nullable=False, index=True)
    stack_order = Column(Integer, default=0, index=True)
    pushed_at = Column(DateTime, default=utc_now)

    title = relationship("MovieTitle")
