"""Central configuration, loaded from environment variables."""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Auth
    jwt_secret: str = "dev-insecure-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # Infra
    database_url: str = "postgresql+asyncpg://devops:devops@db:5432/devops_platform"
    redis_url: str = "redis://redis:6379/0"

    # Content lives on disk as markdown + scripts (git-versionable).
    content_dir: Path = Path("/app/content")

    # Lab engine
    lab_idle_timeout_min: int = 30
    lab_max_duration_min: int = 120
    lab_memory_limit: str = "512m"
    lab_cpu_limit: float = 1.0
    lab_network: str = "devops_labnet"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
