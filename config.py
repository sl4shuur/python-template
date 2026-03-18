"""Typed configuration via pydantic-settings."""

from pathlib import Path
from pprint import pprint
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Directories
    root_dir: Path = Path()
    log_dir: Path = root_dir / "logs"

    directories: list[Path] = [root_dir, log_dir]


config = Config()

for directory in config.directories:
    if directory.exists() and directory.is_file():
        directory.unlink()  # Remove the file if a file exists with the same name
    directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    pprint(config)
