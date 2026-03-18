import json
import logging
from datetime import datetime
from logging.config import dictConfig
from typing import Any

from config import Config, get_config

from src.adapters.logger import CustomLogger
from .logging_formatters import ColoredFormatter


def register_success_level() -> None:
    logging.addLevelName(get_config().success_level, "SUCCESS")


class EvalLogger(CustomLogger):
    def __init__(self, config: Config, name: str = "eval") -> None:
        super().__init__(name)
        self._json_path = config.log_dir / "evaluation.json"
        self._run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def metric(self, label: str, score: float) -> None:
        self.info("%s: %.4f", label, score, extra={
                  "score": score}, stacklevel=2)

    def flush_json(
        self,
        metrics: dict[str, Any],
        extra: dict[str, Any] | None = None,
        false_positives: list[dict[str, Any]] | None = None,
    ) -> None:
        runs: list[dict[str, Any]] = []
        if self._json_path.exists():
            try:
                runs = json.loads(self._json_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                runs = []

        entry: dict[str, Any] = {
            "run_id": self._run_id,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
        }
        if extra:
            entry["extra"] = extra
        if false_positives:
            entry["false_positives"] = false_positives

        runs.append(entry)
        self._json_path.write_text(
            json.dumps(runs, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


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


def get_logger(name: str = "app") -> CustomLogger:
    return CustomLogger(name)


def get_eval_logger(settings: Config, name: str = "eval") -> EvalLogger:
    return EvalLogger(config=settings, name=name)
