from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Anthropic API
    anthropic_api_key: Optional[str] = None

    # Client API Keys (comma-separated for multiple clients)
    api_keys: str = ""  # e.g., "roborder_key_abc123,client2_key_xyz789"

    # Redis Cache
    redis_url: str = "redis://localhost:6379"

    # CORS
    allowed_origins: str = "https://app.roborder.ai"

    # Logging
    log_level: str = "INFO"

    # Reply Generation
    max_tokens_per_reply: int = 200  # Enough for 2 quality sentences

    # Cache TTL (seconds)
    post_summary_ttl: int = 86400  # 24 hours
    recent_replies_ttl: int = 3600  # 1 hour

    # Rate Limiting
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
