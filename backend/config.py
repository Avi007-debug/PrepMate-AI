"""
Configuration management and environment variable loading
"""
from pydantic_settings import BaseSettings
from typing import List, Union


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "PrepMate-AI"

    # CORS
    # Accept either a JSON array in the env or a comma-separated string (common in .env files)
    ALLOWED_ORIGINS: Union[List[str], str] = "http://localhost:5173,http://localhost:3000"

    # LLM / API Keys
    # Prefer GROQ key; OPENAI_API_KEY is kept for backward compatibility.
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # LLM settings (generic)
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.7
    # When True, use deterministic local stubs instead of calling external LLMs
    MOCK_LLM: bool = False

    # Interview Configuration
    MAX_QUESTIONS: int = 10
    QUESTION_DIFFICULTY: str = "medium"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Normalize ALLOWED_ORIGINS: allow comma-separated string in .env files
try:
    if isinstance(settings.ALLOWED_ORIGINS, str):
        settings.ALLOWED_ORIGINS = [s.strip() for s in settings.ALLOWED_ORIGINS.split(",") if s.strip()]
except Exception:
    # Fallback to a safe default list
    settings.ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]

# Backwards-compatible key handling: if GROQ_API_KEY is set prefer it, otherwise fall back to OPENAI_API_KEY
if not settings.OPENAI_API_KEY and settings.GROQ_API_KEY:
    # mirror GROQ into OPENAI_API_KEY so existing code referencing OPENAI_API_KEY continues to work
    settings.OPENAI_API_KEY = settings.GROQ_API_KEY
