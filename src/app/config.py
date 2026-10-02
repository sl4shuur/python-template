"""Application settings and runtime preparation helpers."""

from functools import lru_cache
from pathlib import Path
from pprint import pprint
from typing import Literal

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class LoggingConfig(BaseModel):
    directory: Path = Field(default=Path("logs"), validate_default=True)
    level: str = "INFO"
    formatter: Literal["ColoredFormatter", "ContextualColorFormatter"] = "ColoredFormatter"
    date_format: str = "%d-%m-%Y %H:%M:%S"
    full_color: bool = True
    include_function: bool = True
    success_level: int = Field(default=69, ge=1)

    @field_validator("directory")
    @classmethod
    def _under_project_root(cls, directory: Path) -> Path:
        return PROJECT_ROOT / directory


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_prefix="APP_",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "app"
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


@lru_cache
def get_config() -> Config:
    return Config()


if __name__ == "__main__":
    print(f"{PROJECT_ROOT=}")
    pprint(get_config())
