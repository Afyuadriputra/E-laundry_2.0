from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = "development"
    APP_NAME: str = "Laundry UMKM API"
    DEBUG: bool = True

    DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/laundry_dev"
    )

    SESSION_SECRET: str = Field(
        default="dev_session_secret_key_32_characters_minimum_length_e_laundry"
    )
    CSRF_SECRET: str = Field(default="dev_csrf_secret_key_32_characters_minimum_length_e_laundry")

    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    PUBLIC_BASE_URL: str = "http://localhost:5173"

    LOG_LEVEL: str = "INFO"
    BUSINESS_TIMEZONE: str = "Asia/Jakarta"

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v: Any) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            val = v.strip().lower()
            if val in ("true", "1", "yes", "on", "dev", "development"):
                return True
            if val in ("false", "0", "no", "off", "release", "prod", "production"):
                return False
        return bool(v)

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
