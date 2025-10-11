import logging
from functools import lru_cache

from manakit_assistant.configuration import AssistantConfig
from manakit_commons.configuration.configuration import (
    ApplicationConfig,
    Configuration,
)
from manakit_commons.registry import service_registry
from manakit_imagecreator.configuration import ImageGeneratorConfig
from manakit_user.authentication.configuration import AuthenticationConfiguration

logger = logging.getLogger(__name__)


class AppConfig(ApplicationConfig):
    authentication: AuthenticationConfiguration
    imagegenerator: ImageGeneratorConfig | None = None
    assistant: AssistantConfig | None = None


@lru_cache(maxsize=1)
def configure() -> Configuration[AppConfig]:
    logger.debug("--- Configuring application settings ---")
    return service_registry().configure(
        AppConfig,
        env_file="/.env",
    )
