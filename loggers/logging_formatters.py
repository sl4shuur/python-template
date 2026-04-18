import logging
from colorama import Fore, Style


def _hex_to_ansi(hex_color: str) -> str:
    """Convert hex color to ANSI escape sequence."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i: i + 2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


COLORS = {
    "DEBUG":    _hex_to_ansi("#3ACEFF"),
    "INFO":     _hex_to_ansi("#A1F7FF"),
    "SUCCESS":  _hex_to_ansi("#69FE69"),
    "WARNING":  _hex_to_ansi("#FDF32F"),
    "ERROR":    _hex_to_ansi("#F61C1C"),
    "CRITICAL": _hex_to_ansi("#FF6EFF"),
}

EVAL_THRESHOLDS = [
    ("GOOD", 0.69,  _hex_to_ansi("#69FE69")),
    ("OKAY", 0.4, _hex_to_ansi("#FDF32F")),
    ("POOR", 0.0,  _hex_to_ansi("#F61C1C")),
]


def _get_eval_badge(score: float) -> tuple[str, str]:
    """
    Return (label, ansi_color) based on score thresholds.

    :param score: Float score in range [0, 1].
    :return: Tuple of badge label and ANSI color string.
    """
    for label, threshold, color in EVAL_THRESHOLDS:
        if score >= threshold:
            return label, color
    return "POOR", _hex_to_ansi("#F61C1C")


class ColoredFormatter(logging.Formatter):
    """
    Colored console formatter.

    Supports two layout modes:
    - inline (full_color=False): timestamp on one line, level + message on next
    - block  (full_color=True):  entire output wrapped in level color

    Supports two context modes (mutually exclusive, eval_mode takes priority):
    - include_function: show file path + line + function name
    - eval_mode:        show [GOOD]/[OKAY]/[POOR] badge from record.score
    """

    def __init__(
        self,
        full_color: bool = False,
        include_function: bool = False,
        eval_mode: bool = False,
    ) -> None:
        """
        :param full_color: Wrap entire output in level color block.
        :param include_function: Show file path + line number + function name.
        :param eval_mode: Show score badge instead of function info (requires record.score).
        """
        super().__init__()
        self.full_color = full_color
        self.include_function = include_function
        self.eval_mode = eval_mode

    def _build_context(self, record: logging.LogRecord, log_color: str) -> str | None:
        """
        Build context string: either eval badge or function info.

        :param record: The log record.
        :param log_color: ANSI color for the current log level.
        :return: Formatted context string or None.
        """
        if self.eval_mode:
            score = getattr(record, "score", None)
            if score is not None:
                label, badge_color = _get_eval_badge(float(score))
                if self.full_color:
                    return f"{Style.RESET_ALL}{badge_color}[{label}]{Style.RESET_ALL}{log_color}"
                # Do NOT reset after badge — message color will be applied separately
                return f"{badge_color}[{label}]"

        if self.include_function:
            file_info = f"{record.pathname}:{record.lineno} -> {record.funcName}"
            if self.full_color:
                return f"[{file_info}]"
            return f"{_hex_to_ansi('#76ADF4')}[{file_info}]{Style.RESET_ALL}"

        return None

    def format(self, record: logging.LogRecord) -> str:
        log_color = COLORS.get(record.levelname, Fore.WHITE)
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")

        score = getattr(record, "score", None)

        # Determine message color based on badge if available, otherwise use level color
        has_score = False
        if self.eval_mode and score is not None:
            has_score = True
            _, message_color = _get_eval_badge(float(score))
        else:
            message_color = log_color

        # Build context AFTER message_color is determined
        context = self._build_context(record, log_color)

        if self.full_color:
            parts = [f"[{timestamp}]"]
            if context:
                parts.append(context)
            header = " ".join(parts)
            if has_score:
                block = f"\n{header}{Style.RESET_ALL}\n{message_color}{record.getMessage()}"
                return f"{message_color}{block}{Style.RESET_ALL}"
            block = f"\n{header}\n{record.levelname}: {record.getMessage()}"
            return f"{message_color}{block}{Style.RESET_ALL}"

        # Inline mode
        colored_time = f"{message_color}{timestamp}{Style.RESET_ALL}"
        parts = [f"[{colored_time}]"]
        if context:
            parts.append(context)
        header = " ".join(parts)

        if has_score:
            return f"{header} {message_color}{record.getMessage()}{Style.RESET_ALL}"

        colored_level = f"{message_color}{record.levelname}{Style.RESET_ALL}"
        return f"{header}\n{colored_level}: {message_color}{record.getMessage()}{Style.RESET_ALL}"
