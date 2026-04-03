import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root@localhost:3306/autofill_db"
    )
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AutoFill AI System"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
    ]
    
    # AI Configuration
    TOP_SUGGESTIONS_COUNT: int = 3
    HISTORY_LOOKBACK_DAYS: int = 30
    MIN_HISTORY_ENTRIES: int = 5
    
    # AI Composer Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")  # 'openai' | 'gemini' | 'openrouter'
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4o-mini")

    # OpenRouter Configuration (OpenAI-compatible endpoint)
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-120b:free")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    OPENROUTER_SITE_URL: str = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8000")
    OPENROUTER_APP_NAME: str = os.getenv("OPENROUTER_APP_NAME", "AutoFill AI System")

    COMPOSER_MAX_SUGGESTIONS: int = 3
    COMPOSER_SUGGESTION_LENGTH: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
