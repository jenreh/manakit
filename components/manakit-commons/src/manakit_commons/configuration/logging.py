import logging.config
from pathlib import Path

import yaml

from manakit_commons import CONFIGURATION_PATH
from manakit_commons.configuration.configuration import Configuration

logger = logging.getLogger(__name__)


def init_logging(configuration: Configuration) -> None:
    # check if profile based logging configuration exists
    log_configuration = configuration.app.logging
    if CONFIGURATION_PATH.joinpath(log_configuration).exists():
        logger.info(
            "Using logging configuration: \x1b[31;1m%s\x1b[0m", log_configuration
        )
        with Path.open(
            CONFIGURATION_PATH / log_configuration, "rt", encoding="utf-8"
        ) as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logger.info("Using logging configuration: \x1b[31;1mlogging.conf\x1b[0m")
