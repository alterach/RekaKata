"""Application configuration settings."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Groq API Configuration
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    groq_temperature: float = 0.7
    groq_max_tokens: int = 2048

    # Telegram Bot Configuration
    telegram_bot_token: str

    # Application Paths
    log_level: str = "INFO"
    output_dir: str = "output"
    data_dir: str = "data"
    config_dir: str = "config"

    # Platform Defaults
    default_platforms: str = "tiktok,instagram,youtube"
    default_aspect_ratio: str = "9:16"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def platforms_list(self) -> list[str]:
        """Return platforms as a list."""
        return [p.strip() for p in self.default_platforms.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
