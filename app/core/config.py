"""Application configuration settings."""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Project info
    PROJECT_NAME: str = "FastAPI Web Application"
    PROJECT_DESCRIPTION: str = "A production-ready FastAPI application with validation, error handling, and testing"
    VERSION: str = "0.1.0"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_HOSTS: List[str] = ["*"]

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
