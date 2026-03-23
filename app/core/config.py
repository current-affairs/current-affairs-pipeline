from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    # ========================
    # App Config
    # ========================
    APP_NAME: str = "Current Affairs Pipeline"
    ENV: str = "dev"

    # ========================
    # Database
    # ========================
    DATABASE_URL: str

    # ========================
    # Redis / Queue
    # ========================
    REDIS_URL: str

    # ========================
    # Security
    # ========================
    # API_KEY: str

    # ========================
    # ML / Embeddings
    # ========================
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_CHAT_MODEL: str
    AZURE_OPENAI_VERSION: str

    # ========================
    # Storage (future)
    # ========================
    # S3_BUCKET: str | None = None

    # ========================
    # Behavior
    # ========================
    REQUEST_TIMEOUT: int = 10
    MAX_RETRIES: int = 3
    

    model_config = SettingsConfigDict(
        env_file=None,  # Don't use .env file
        case_sensitive=True,
        extra='ignore'  # Ignore extra environment variables
    )


# Singleton
@lru_cache
def get_settings() -> Settings:
    return Settings()


# global instance
settings = get_settings()