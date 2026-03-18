import logging
from collections.abc import Callable
from logging.config import dictConfig
from typing import Any, ParamSpec, TypeVar

from config import Config, get_config
from .logging_formatters import ColoredFormatter


P = ParamSpec("P")
TLogger = TypeVar("TLogger", bound=logging.LoggerAdapter)


def register_success_level() -> None:
    logging.addLevelName(get_config().success_level, "SUCCESS")


def build_logging_config(settings: Config) -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": ColoredFormatter,
                "full_color": settings.log_full_color,
                "include_function": settings.log_include_function,
            },
            "eval_console": {
                "()": ColoredFormatter,
                "full_color": settings.log_full_color,
                "eval_mode": True,
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "app_file": {
                "class": "logging.FileHandler",
                "level": settings.log_level,
                "formatter": "standard",
                "filename": str(settings.log_dir / "app.log"),
                "encoding": "utf-8",
            },
            "eval_console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "eval_console",
                "stream": "ext://sys.stdout",
            },
            "eval_file": {
                "class": "logging.FileHandler",
                "level": settings.log_level,
                "formatter": "standard",
                "filename": str(settings.log_dir / "evaluation.log"),
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["console", "app_file"],
        },
        "loggers": {
            "eval": {
                "level": settings.log_level,
                "handlers": ["eval_console", "eval_file"],
                "propagate": False,
            },
        },
    }


def configure_logging(settings: Config) -> None:
    register_success_level()
    dictConfig(build_logging_config(settings))


def get_logger(
    logger_factory: Callable[P, TLogger],
    *args: P.args,
    **kwargs: P.kwargs,
) -> TLogger:
    return logger_factory(*args, **kwargs)
