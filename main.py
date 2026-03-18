import logging
from src.utils.logging import ColoredLogger


def main():
    logger = ColoredLogger.create(name="app", level=logging.DEBUG, full_color=True, include_function=True)
    logger.success("Logging configuration test completed.")


if __name__ == "__main__":
    main()
