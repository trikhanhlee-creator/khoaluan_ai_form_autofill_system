import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/autofill_db"
    )
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AutoFill AI System"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # AI Configuration
    TOP_SUGGESTIONS_COUNT: int = 3
    HISTORY_LOOKBACK_DAYS: int = 30
    MIN_HISTORY_ENTRIES: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
