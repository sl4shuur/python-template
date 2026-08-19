import logging

from colorama import Style

from app.config import Config
from app.loggers.custom_loggers import EvalLogger
from app.loggers.logging_formatters import ColoredFormatter, EvalFileFormatter


def _record() -> logging.LogRecord:
    record = logging.LogRecord(
        name="app.services.pipeline",
        level=logging.INFO,
        pathname="pipeline.py",
        lineno=89,
        msg="hello %s",
        args=("world",),
        exc_info=None,
    )
    return record


def _eval_record(score: float) -> logging.LogRecord:
    record = _record()
    record.score = score
    return record


def test_compact_formatter_can_disable_colors() -> None:
    formatter = ColoredFormatter(full_color=False)
    output = formatter.format(_record())

    assert "\033[38;2;" not in output
    assert "INFO" in output
    assert "[app.services.pipeline:89]" in output
    assert output.endswith("hello world")


def test_compact_formatter_can_hide_location() -> None:
    formatter = ColoredFormatter(full_color=False, include_function=False)
    output = formatter.format(_record())

    assert "[app.services.pipeline:89]" not in output
    assert "INFO" in output
    assert output.endswith("hello world")


def test_compact_formatter_colors_time_level_and_location_by_default() -> None:
    formatter = ColoredFormatter()

    output = formatter.format(_record())

    assert output.count("\033[38;2;") == 3
    assert "[app.services.pipeline:89]" in output
    assert output.endswith("  hello world")


def test_compact_formatter_formats_poor_eval_record() -> None:
    formatter = ColoredFormatter(full_color=False)
    output = formatter.format(_eval_record(0.1234))

    assert "POOR" in output
    assert "POOR      " not in output
    assert "INFO" not in output
    assert "[app.services.pipeline:89]" not in output
    assert output.endswith("hello world")


def test_compact_formatter_formats_okay_eval_record() -> None:
    formatter = ColoredFormatter(full_color=False)
    output = formatter.format(_eval_record(0.5678))

    assert "OKAY" in output
    assert "INFO" not in output
    assert "[app.services.pipeline:89]" not in output


def test_compact_formatter_formats_good_eval_record() -> None:
    formatter = ColoredFormatter(full_color=False)
    output = formatter.format(_eval_record(0.6969))

    assert "GOOD" in output
    assert "INFO" not in output
    assert "[app.services.pipeline:89]" not in output


def test_compact_formatter_colors_whole_eval_row() -> None:
    formatter = ColoredFormatter()
    output = formatter.format(_eval_record(0.6969))

    assert output.startswith("\033[38;2;105;254;105m")
    assert output.endswith(f"hello world{Style.RESET_ALL}")


def test_eval_logger_routes_named_loggers_under_eval_namespace(tmp_path) -> None:
    config = Config(log_dir=tmp_path)
    logger = EvalLogger(config=config, name="main")

    assert logger.logger.name == "eval.main"


def test_eval_file_formatter_uses_score_level() -> None:
    formatter = EvalFileFormatter(date_format="%Y")
    output = formatter.format(_eval_record(0.1234))

    assert output.startswith("2026 [POOR] ")
    assert "[INFO]" not in output
    assert output.endswith("hello world")
