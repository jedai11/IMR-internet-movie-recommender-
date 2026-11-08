from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "MoodReel API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./moodreel.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]
    
    # LLM API configuration (optional)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "auto"  # 'gemini', 'openai', or 'heuristic'
    
    # Weight Engine thresholds (Phase 1)
    COLD_START_THRESHOLD: int = 3
    COLD_START_W_MOOD: float = 0.90
    COLD_START_W_TASTE: float = 0.10
    ESTABLISHED_W_MOOD: float = 0.70
    ESTABLISHED_W_TASTE: float = 0.30
    DEFAULT_W_NOVELTY: float = 0.00
    
    # Shift trajectory step factor lambda (range [0.3, 0.7])
    SHIFT_STEP_FACTOR: float = 0.55
    
    # Distress Safeguard trigger keywords & phrases
    DISTRESS_KEYWORDS: List[str] = [
        "suicide", "kill myself", "end my life", "want to die", 
        "self harm", "cutting myself", "hanging myself", "overdose",
        "jump off", "better off dead", "can't go on anymore",
        "no reason to live", "ending it all", "don't want to wake up"
    ]
    
    # Support helpline resources (International coverage)
    SUPPORT_HELPLINES: List[dict] = [
        {"name": "988 Suicide & Crisis Lifeline", "contact": "Call or Text 988 (US & Canada)", "url": "https://988lifeline.org"},
        {"name": "Crisis Text Line", "contact": "Text HOME to 741741 (US/CA) or 85258 (UK)", "url": "https://www.crisistextline.org"},
        {"name": "Samaritans / NHS 111", "contact": "Call 116 123 (UK & Ireland)", "url": "https://www.samaritans.org"},
        {"name": "Tele-MANAS & KIRAN", "contact": "Call 14416 or 1800-599-0019 (India)", "url": "https://telemanas.mohfw.gov.in"},
        {"name": "Find A Helpline (Worldwide)", "contact": "Free confidential help in 130+ countries", "url": "https://findahelpline.com"},
        {"name": "Befrienders Worldwide", "contact": "Global network of emotional support centers", "url": "https://www.befrienders.org"}
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

