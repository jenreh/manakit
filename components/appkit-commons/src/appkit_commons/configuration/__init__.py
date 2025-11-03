import importlib
from typing import Any

from appkit_commons.configuration.base import BaseConfig
from appkit_commons.configuration.secret_provider import (
    SecretNotFoundError,
    SecretProvider,
    get_secret,
)
from appkit_commons.configuration.yaml import (
    YamlConfigReader,
    YamlConfigSettingsSource,
)
# Remove this direct import that causes the circular dependency
# from appkit_commons.configuration.logging import init_logging

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
    "Configuration": "appkit_commons.configuration.configuration",
    "ApplicationConfig": "appkit_commons.configuration.configuration",
    "DatabaseConfig": "appkit_commons.configuration.configuration",
    "ServerConfig": "appkit_commons.configuration.configuration",
    "WorkerConfig": "appkit_commons.configuration.configuration",
    "Protocol": "appkit_commons.configuration.configuration",
    "init_logging": "appkit_commons.configuration.logging",
}


def __getattr__(name: str) -> Any:
    module_path = _lazy_map.get(name)
    if module_path is None:
        raise AttributeError(
            f"module 'appkit_commons.configuration' has no attribute {name!r}"
        )
    module = importlib.import_module(module_path)
    return getattr(module, name)
