"""
Configuration settings for Pain Management Support Group API
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    APP_NAME: str = "Pain Management Support Group API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pain_management"
    DB_ECHO: bool = False

    # Redis (for Celery and caching)
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 300  # 5 minutes

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"

    # Anthropic Claude (alternative to OpenAI)
    ANTHROPIC_API_KEY: Optional[str] = None

    # Vector Database - Pinecone
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: str = "us-west1-gcp"
    PINECONE_INDEX_NAME: str = "pain-management-docs"

    # ChromaDB (local alternative)
    CHROMA_DB_PATH: str = "./rag/chromadb"
    USE_PINECONE: bool = False  # Toggle between Pinecone and ChromaDB

    # Document Processing
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".txt", ".md"]
    DOCUMENTS_PATH: str = "./rag/documents"

    # RAG Settings
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7

    # Email (for notifications)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@painmanagement.com"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # Assessment Settings
    PRE_TEST_QUESTIONS: int = 15
    POST_TEST_QUESTIONS: int = 15
    PASSING_SCORE: float = 70.0

    # Session Settings
    SESSION_DURATION_MINUTES: int = 150  # 2.5 hours
    TOTAL_WEEKS: int = 8
    SESSIONS_PER_WEEK: int = 4

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Create settings instance
settings = get_settings()
