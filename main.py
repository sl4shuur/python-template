from src.services import setup
from src.utils.logging import CustomLogger, EvalLogger, get_logger


def main() -> None:
    config = setup()
    logger = get_logger(CustomLogger, "app")
    eval_logger = get_logger(EvalLogger, config, "eval")
    logger.success("Application started successfully.")
    eval_logger.metric("Accuracy", 0.69)
    eval_logger.flush_json(
        metrics={"accuracy": 0.69},
        extra={"model": "example-model"},
        false_positives=[{"id": 1, "text": "False positive example"}],
    )


if __name__ == "__main__":
    main()
