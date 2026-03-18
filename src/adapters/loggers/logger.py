import logging
from typing import Any

from config import get_config


class CustomLogger(logging.LoggerAdapter):
    def __init__(self, name: str = "app") -> None:
        super().__init__(logging.getLogger(name), extra={})

    def success(self, message: str, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("stacklevel", 2)
        self.logger.log(get_config().success_level, message, *args, **kwargs)
