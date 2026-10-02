import logging
from collections.abc import Callable
from logging.config import dictConfig
from typing import Any

from app.config import Config

from .logging_formatters import ColoredFormatter, ContextualColorFormatter

FORMATTERS: dict[str, type[logging.Formatter]] = {
    ColoredFormatter.__name__: ColoredFormatter,
    ContextualColorFormatter.__name__: ContextualColorFormatter,
}


def build_logging_config(config: Config) -> dict[str, Any]:
    log = config.logging
    console_formatter = FORMATTERS[log.formatter]

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": console_formatter,
                "full_color": log.full_color,
                "include_function": log.include_function,
                "date_format": log.date_format,
            },
            "eval_console": {
                "()": console_formatter,
                "full_color": log.full_color,
                "include_function": log.include_function,
                "date_format": log.date_format,
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": log.date_format,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log.level,
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "eval_console": {
                "class": "logging.StreamHandler",
                "level": log.level,
                "formatter": "eval_console",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": log.level,
            "handlers": ["console"],
        },
        "loggers": {
            "eval": {
                "level": log.level,
                "handlers": ["eval_console"],
                "propagate": False,
            },
        },
    }


def apply_logging_config(config: Config) -> None:
    logging.addLevelName(config.logging.success_level, "SUCCESS")
    dictConfig(build_logging_config(config))


def get_logger[**P, TLogger: logging.LoggerAdapter](
    logger_factory: Callable[P, TLogger],
    *args: P.args,
    **kwargs: P.kwargs,
) -> TLogger:
    return logger_factory(*args, **kwargs)
