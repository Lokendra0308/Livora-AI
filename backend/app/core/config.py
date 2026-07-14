"""
Centralized application configuration.

Why this pattern:
- All environment-driven config lives in ONE typed object (Settings).
- Pydantic validates types/values at startup, so a bad .env fails fast
  instead of causing a mysterious bug three requests later.
- Every other module imports `settings` instead of calling os.getenv()
  directly, so there is exactly one source of truth.
"""

from functools import lru_cache
from typing import List, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- General ---
    APP_NAME: str = "Nexus AI"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --- Security / Auth ---
    JWT_SECRET_KEY: str = Field(default="change-me-in-env", repr=False)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # --- CORS ---
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # --- Database ---
    DATABASE_URL: str = "sqlite:///./nexus.db"

    # --- Vector store ---
    CHROMA_PERSIST_DIR: str = "./chroma_store"

    # --- LLM Providers (all optional — only the ones you configure are used) ---
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_LLM_PROVIDER: Literal["openai", "gemini", "groq", "ollama"] = "groq"

    # --- Embeddings ---
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # --- Rate limiting ---
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings accessor.

    lru_cache ensures the .env file is parsed once per process, not on
    every request — Settings() is cheap but not free, and this keeps
    config immutable/consistent for the app's lifetime.
    """
    return Settings()


settings = get_settings()
