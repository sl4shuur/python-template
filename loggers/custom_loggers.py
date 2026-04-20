import json
import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from config import Config, get_config


class CustomLogger(logging.LoggerAdapter):
    def __init__(self, name: str = "app") -> None:
        super().__init__(logging.getLogger(name), extra={})

    def success(self, message: str, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("stacklevel", 2)
        self.logger.log(get_config().success_level, message, *args, **kwargs)


class EvalLogger(logging.LoggerAdapter):
    def __init__(self, config: Config, name: str = "eval") -> None:
        logger_name = name if name == "eval" or name.startswith("eval.") else f"eval.{name}"
        super().__init__(logging.getLogger(logger_name), {})

        self._json_path = config.log_dir / "evaluation.json"
        self._run_id = datetime.now().strftime(config.log_date_format)

    def process(
        self,
        msg: Any,
        kwargs: dict[str, Any],
    ) -> tuple[Any, dict[str, Any]]:
        extra = dict(self.extra) if self.extra else {}
        record_extra = kwargs.get("extra")

        if isinstance(record_extra, Mapping):
            extra.update(record_extra)

        kwargs["extra"] = extra
        return msg, kwargs

    def metric(self, label: str, score: float) -> None:
        self.info("%s: %.4f", label, score, extra={"score": score}, stacklevel=2)

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
