import logging

import reflex as rx

from manakit_commons.configuration.configuration import ReflexConfig
from manakit_commons.configuration.logging import init_logging
from manakit_commons.database.configuration import DatabaseConfig
from manakit_commons.registry import service_registry

from app import configuration

init_logging(configuration)
logger = logging.getLogger(__name__)

database: DatabaseConfig | None = service_registry().get(DatabaseConfig)
reflex: ReflexConfig | None = service_registry().get(ReflexConfig)

logger.debug("Database URL: %s", database.url)

config = rx.Config(
    app_name="app",
    frontend_port=reflex.frontend_port if reflex else 8080,
    backend_port=reflex.backend_port if reflex else 3030,
    gunicorn_workers=reflex.workers if reflex else 1,
    db_url=database.url,
    async_db_url=database.url,
    telemetry_enabled=False,
    show_built_with_reflex=False,
    plugins=[
        # rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
