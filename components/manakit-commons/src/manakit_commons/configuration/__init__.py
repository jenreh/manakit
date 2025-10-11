import importlib
from typing import Any

from manakit_commons.configuration.base import BaseConfig
from manakit_commons.configuration.secret_provider import (
    SecretNotFoundError,
    SecretProvider,
    get_secret,
)
from manakit_commons.configuration.yaml import (
    YamlConfigReader,
    YamlConfigSettingsSource,
)
# Remove this direct import that causes the circular dependency
# from manakit_commons.configuration.logging import init_logging

__all__ = [
    "ApplicationConfig",
    "BaseConfig",
    "Configuration",
    "DatabaseConfig",
    "Protocol",
    "SecretNotFoundError",
    "SecretProvider",
    "ServerConfig",
    "WorkerConfig",
    "YamlConfigReader",
    "YamlConfigSettingsSource",
    "get_secret",
    "init_logging",
]

# Keep backward compatibility if someone used the wrong name
__ALL__ = __all__

_lazy_map: dict[str, str] = {
    "Configuration": "manakit_commons.configuration.configuration",
    "ApplicationConfig": "manakit_commons.configuration.configuration",
    "DatabaseConfig": "manakit_commons.configuration.configuration",
    "ServerConfig": "manakit_commons.configuration.configuration",
    "WorkerConfig": "manakit_commons.configuration.configuration",
    "Protocol": "manakit_commons.configuration.configuration",
    "init_logging": "manakit_commons.configuration.logging",
}


def __getattr__(name: str) -> Any:
    module_path = _lazy_map.get(name)
    if module_path is None:
        raise AttributeError(
            f"module 'manakit_commons.configuration' has no attribute {name!r}"
        )
    module = importlib.import_module(module_path)
    return getattr(module, name)
