"""Application orchestration, independent of the command-line interface."""

from app.config import get_config
from app.loggers import CustomLogger, EvalLogger, get_logger


def run() -> int:
    """Run the application."""
    config = get_config()
    logger = get_logger(CustomLogger, name=__name__)
    eval_logger = get_logger(EvalLogger, config=config, name=__name__)

    eval_logger.metric("example_metric", 0.5234)
    logger.success("This is a success message.")

    return 0
