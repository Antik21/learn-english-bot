from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: str = Field(alias="BOT_TOKEN")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/app.sqlite3",
        alias="DATABASE_URL",
    )
    amplitude_enabled: bool = Field(default=False, alias="AMPLITUDE_ENABLED")
    amplitude_api_key: str | None = Field(default=None, alias="AMPLITUDE_API_KEY")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
