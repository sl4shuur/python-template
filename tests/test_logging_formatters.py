import logging

from loggers.logging_formatters import ColoredFormatter


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
