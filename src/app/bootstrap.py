"""Application startup: wires the configuration into the runtime."""

from app.config import Config
from app.loggers import apply_logging_config


def bootstrap(config: Config) -> None:
    """Prepare the runtime. Call once, before the application starts logging."""
    apply_logging_config(config)
