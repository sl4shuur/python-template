import logging
from collections.abc import Callable
from logging.config import dictConfig
from typing import Any

from config import Config

from .logging_formatters import ColoredFormatter, ContextualColorFormatter

FORMATTERS: dict[str, type[logging.Formatter]] = {
    ColoredFormatter.__name__: ColoredFormatter,
    ContextualColorFormatter.__name__: ContextualColorFormatter,
}


def build_logging_config(config: Config) -> dict[str, Any]:
    console_formatter = FORMATTERS[config.log_formatter]

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": console_formatter,
                "full_color": config.log_full_color,
                "include_function": config.log_include_function,
                "date_format": config.log_date_format,
            },
            "eval_console": {
                "()": ContextualColorFormatter,
                "full_color": config.log_full_color,
                "eval_mode": True,
                "date_format": config.log_date_format,
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": config.log_date_format,
            },
            "eval_standard": {
                "format": "%(asctime)s [%(levelname)s] %(message)s",
                "datefmt": config.log_date_format,
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
                "formatter": "eval_standard",
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
    logging.addLevelName(config.success_level, "SUCCESS")
    dictConfig(build_logging_config(config))


def get_logger[**P, TLogger: logging.LoggerAdapter](
    logger_factory: Callable[P, TLogger],
    *args: P.args,
    **kwargs: P.kwargs,
) -> TLogger:
    return logger_factory(*args, **kwargs)
