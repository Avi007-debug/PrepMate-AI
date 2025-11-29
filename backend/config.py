"""
Configuration management and environment variable loading
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "PrepMate-AI"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # OpenAI/LLM Configuration
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.7
    
    # Interview Configuration
    MAX_QUESTIONS: int = 10
    QUESTION_DIFFICULTY: str = "medium"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
