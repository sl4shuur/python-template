from config import Config, get_config, prepare_runtime
from loggers import configure_logging


def setup() -> Config:
    config = get_config()
    prepare_runtime(config)
    configure_logging(config)
    return config
