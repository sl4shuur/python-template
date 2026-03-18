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


def build_logging_config(config: Config) -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": ColoredFormatter,
                "full_color": config.log_full_color,
                "include_function": config.log_include_function,
            },
            "eval_console": {
                "()": ColoredFormatter,
                "full_color": config.log_full_color,
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
                "level": config.log_level,
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "app_file": {
                "class": "logging.FileHandler",
                "level": config.log_level,
                "formatter": "standard",
                "filename": str(config.log_dir / "app.log"),
                "encoding": "utf-8",
            },
            "eval_console": {
                "class": "logging.StreamHandler",
                "level": config.log_level,
                "formatter": "eval_console",
                "stream": "ext://sys.stdout",
            },
            "eval_file": {
                "class": "logging.FileHandler",
                "level": config.log_level,
                "formatter": "standard",
                "filename": str(config.log_dir / "evaluation.log"),
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": config.log_level,
            "handlers": ["console", "app_file"],
        },
        "loggers": {
            "eval": {
                "level": config.log_level,
                "handlers": ["eval_console", "eval_file"],
                "propagate": False,
            },
        },
    }


def configure_logging(config: Config) -> None:
    register_success_level()
    dictConfig(build_logging_config(config))


def get_logger(
    logger_factory: Callable[P, TLogger],
    *args: P.args,
    **kwargs: P.kwargs,
) -> TLogger:
    return logger_factory(*args, **kwargs)
