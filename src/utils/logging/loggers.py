import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Self

from src.interfaces import ILogger
from config import config
from .logging_formatters import ColoredFormatter


SUCCESS_LEVEL = 69
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


class ColoredLogger(ILogger):
    """Colored console logger with SUCCESS level."""

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        super().__init__(name, level)

    @classmethod
    def create(
        cls,
        name: str = "app",
        level: int = logging.INFO,
        full_color: bool = False,
        include_function: bool = False,
    ) -> Self:
        """
        Factory method to create a configured ColoredLogger.

        :param name: Logger name.
        :param level: Logging level.
        :param full_color: Use block color layout.
        :param include_function: Show file path + line + function name.
        :return: Configured ColoredLogger instance.
        """
        logging.setLoggerClass(cls)
        logger = logging.getLogger(name)

        # Clear existing handlers to avoid duplication on re-runs
        if logger.handlers:
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)

        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColoredFormatter(
            full_color=full_color, include_function=include_function))
        logger.addHandler(handler)

        return logger  # type: ignore[return-value]

    def success(self, message: str, *args, **kwargs) -> None:
        """Log a message with SUCCESS level."""
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, message, args, stacklevel=2, **kwargs)


class EvalLogger(ILogger):
    """
    Evaluation metrics logger.
    Writes colored output to console and appends results to a JSON file.
    """

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        super().__init__(name, level)
        self._json_path: Path | None = None
        self._run_id: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._metrics: dict[str, Any] = {}

    @classmethod
    def create(
        cls,
        name: str = "eval",
        level: int = logging.INFO,
        log_file_name: str = "evaluation.log",
        json_file_name: str = "evaluation.json",
        full_color: bool = False,
    ) -> Self:
        """
        Factory method to create a configured EvalLogger.

        :param name: Logger name.
        :param level: Logging level.
        :param log_file_name: Name of the log file (stored in LOGS_DIR).
        :param json_file_name: Name of the JSON file for metrics (stored in LOGS_DIR).
        :param full_color: Use block color layout on console.
        :return: Configured EvalLogger instance.
        """
        logging.setLoggerClass(cls)
        logger: cls = logging.getLogger(name)  # type: ignore[assignment]

        # Clear existing handlers to avoid duplication on re-runs
        if logger.handlers:
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)

        logger.setLevel(level)

        # Console handler — colored with eval badge support
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter(
            full_color=full_color, eval_mode=True))
        logger.addHandler(console_handler)

        # Plain text file handler
        log_file = config.log_dir / log_file_name
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        logger.addHandler(file_handler)

        # Store JSON path for metric flushing
        json_file = config.log_dir / json_file_name
        logger._json_path = json_file

        return logger  # type: ignore[return-value]

    def metric(self, label: str, score: float) -> None:
        """
        Log a single evaluation metric with a score-based badge.
        Accumulates the metric for JSON export (call flush_json() to write).

        :param label: Metric name (e.g. "Answer Accuracy").
        :param score: Float score in range [0, 1].

        Example:
            logger.metric("Answer Accuracy", 0.711)
            logger.metric("Document Accuracy", 0.0)
            logger.flush_json()
        """
        self._metrics[label] = round(score, 4)
        display = f"{label}: {score:.4f}"
        self._log(logging.INFO, display, (), extra={
                  "score": score}, stacklevel=2)

    def flush_json(
        self,
        metrics: dict[str, Any],
        extra: dict[str, Any] | None = None,
        false_positives: list[dict[str, Any]] | None = None,
    ) -> None:
        """
        Write metrics to the JSON file.
        Appends a new run entry — existing data is preserved.

        :param metrics: Full metrics dict to store (e.g. {"final_score": 0.08, "domain_1": {...}}).
        :param extra: Optional extra fields to include in the run entry (e.g. engine name).
        :param false_positives: Optional list of wrong predictions with details.
        """
        if not self._json_path:
            return

        runs: list[dict] = []
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

        self._metrics.clear()
        print(f"Results saved to {self._json_path}")

    def success(self, message: str, *args, **kwargs) -> None:
        """Log a message with SUCCESS level."""
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, message, args, stacklevel=2, **kwargs)