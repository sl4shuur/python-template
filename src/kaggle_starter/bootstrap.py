"""Application startup: wires the configuration into the runtime."""

from functools import lru_cache

from kaggle_starter.config import Config, get_config
from kaggle_starter.core.errors import ConfigurationError
from kaggle_starter.loggers import apply_logging_config


@lru_cache
def bootstrap() -> Config:
    try:
        config = get_config()
        config.logging.directory.mkdir(parents=True, exist_ok=True)
        apply_logging_config(config.logging)
    except Exception as error:
        raise ConfigurationError(f"Could not bootstrap the application: {error}") from error
    return config
