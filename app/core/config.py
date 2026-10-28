from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "WellPro Intelligence Service"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Frappe Integration
    FRAPPE_BASE_URL: str = Field(default="http://localhost:8000")

    # MongoDB Atlas
    MONGODB_URL: str = Field(...)
    MONGODB_DB_NAME: str = Field(default="wellpro_db")

    # Gemini AI
    GEMINI_API_KEY: str = Field(...)
    GROQ_API_KEY: str

    LANGSMITH_TRACING: str = "true"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: str = "wellpro-co-pilot"

    OPENROUTER_API_KEY: str
    OPENROUTER_VISION_MODEL: str = "openrouter/free"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()