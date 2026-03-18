import logging
from abc import ABC, abstractmethod


class ILogger(logging.Logger, ABC):
    """Interface for a custom logger with an additional SUCCESS level."""

    @abstractmethod
    def success(self, message: str, *args, **kwargs) -> None:
        """Log a message with custom SUCCESS level."""
        pass
