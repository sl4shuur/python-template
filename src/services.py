from config import get_config, prepare_runtime, Config
from src.utils.logging.loggers import configure_logging


def setup() -> Config:
    config = get_config()
    prepare_runtime(config)
    configure_logging(config)
    return config
