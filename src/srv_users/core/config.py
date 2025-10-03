from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from pathlib import Path
import os

# ROOT_DIR = Path(__file__).resolve().parents[3]
# ENV_FILE = ROOT_DIR / ".env"

class Settings(BaseSettings):
    app_name: str = "srv_users"
    environment: str = "dev"
    database_url: AnyUrl
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="SRV_USERS_",
        env_file=str(".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        secrets_dir=None if os.name == "nt" else "/run/secrets",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()