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

    # LLM / API Keys
    # Prefer GROQ key; OPENAI_API_KEY is kept for backward compatibility.
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # LLM settings (generic)
    LLM_MODEL: str = "llama-3.1-70b-versatile"  # Default GROQ model
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

# Backwards-compatible key handling: if GROQ_API_KEY is set prefer it, otherwise fall back to OPENAI_API_KEY
if not settings.OPENAI_API_KEY and settings.GROQ_API_KEY:
    # mirror GROQ into OPENAI_API_KEY so existing code referencing OPENAI_API_KEY continues to work
    settings.OPENAI_API_KEY = settings.GROQ_API_KEY
