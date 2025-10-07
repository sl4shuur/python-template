import logging
import sys

from logging_formatters import ColoredFormatter, FullColoredFormatter

# Success level for logging (custom level)
SUCCESS_LEVEL = 69
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


def success(self, message, *args, stacklevel=3, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self.log(SUCCESS_LEVEL, message, *args,
                 stacklevel=stacklevel, **kwargs)


# Add the success method to the Logger class
setattr(logging.Logger, "success", success)


# Adding a module-level function for logging
def logging_success(message, *args, **kwargs):
    logging.getLogger().success(message, *args, **kwargs)


logging.success = logging_success


def setup_logging( level: int = logging.INFO, full_color: bool = False, include_function: bool = False) -> None:
    """
    Setup logging configuration with colored output and optional function names.

    Args:
        level (int, optional): Logging level, by default logging.INFO
        full_color (bool, optional): Enable full color output, by default False
        include_function (bool, optional): Include function name in logs, by default False

    Returns:
        None

    Example:
        ```python
        import logging
        from utils.logging_config import setup_logging
        setup_logging(level=logging.DEBUG, full_color=True, include_function=True)
        logger = logging.getLogger(__name__)
        logger.debug("This is a debug message.")
        ```
    """
    handler = logging.StreamHandler(sys.stdout)

    if full_color:
        handler.setFormatter(FullColoredFormatter(
            include_function=include_function))
    else:
        handler.setFormatter(ColoredFormatter(
            include_function=include_function))

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Reduce noise from external libraries
    logging.getLogger("aio_pika").setLevel(logging.WARNING)
    logging.getLogger("opentelemetry").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    if include_function:
        logging.success("🎨 Colored logging configured with function names")
    else:
        logging.success("🎨 Colored logging configured")


def logging_test_func():
    """
    Test function to demonstrate logging setup.
    This function will log messages at various levels.
    """
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.success("This is a success message!")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")


if __name__ == "__main__":
    print("Regular color logging:")
    setup_logging(level=logging.DEBUG)
    logging_test_func()

    print("\nFull color logging:")
    logging.getLogger().handlers.clear()
    setup_logging(level=logging.DEBUG, full_color=True)
    logging_test_func()

    print("\nFull color logging with tracing and function names:")
    setup_logging(level=logging.DEBUG, full_color=True, include_function=True)
    logging_test_func()
