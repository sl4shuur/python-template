"""Application settings and runtime preparation helpers."""

from functools import lru_cache
from pathlib import Path
from pprint import pprint

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "app"

    root_dir: Path = PROJECT_ROOT
    log_dir: Path = PROJECT_ROOT / "logs"
    directories: tuple[Path, ...] = (log_dir,)

    log_level: str = "INFO"
    log_full_color: bool = True
    log_include_function: bool = True
    success_level: int = 69


@lru_cache
def get_config() -> Config:
    return Config()


def prepare_runtime(config: Config) -> None:
    for directory in config.directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    pprint(get_config())
