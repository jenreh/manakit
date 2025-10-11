from typing import Final

import reflex as rx
from knai_anonymizer.pages import ANONYMIZER_ROLE
from knai_assistant import ASSISTANT_ROLE
from knai_avvia import AVVIA_PROJECT_ROLE, AVVIA_TENANT_ROLE
from knai_common import styles
from knai_hours import TEAM_MANAGER_ROLE
from knai_nmxdia import INTERNAL_ROLE

from manakit_commons.registry import service_registry
from manakit_imagegen.pages import IMAGE_GENERATOR_ROLE
from manakit_ui.authentication.components import requires_role
from manakit_ui.components.navbar import (
    admin_sidebar_item,
    navbar,
    sidebar_item,
    sub_heading_styles,
)

from app.configuration import AppConfig

_config = service_registry().get(AppConfig)
VERSION: Final[str] = (
    f"{_config.version}-{_config.environment}"
    if _config.environment
    else _config.version
)


def navbar_header() -> rx.Component:
    return rx.hstack(
        rx.image(
            "/img/logo.svg", height="66px", margin_top="1.2em", margin_left="-12px"
        ),
        rx.spacer(),
        align="center",
        width="100%",
        padding="0.35em",
        margin_bottom="1em",
        margin_top="-0.5em",
    )


def navbar_admin_items() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("settings", size=18),
            rx.text("Administration"),
            align="center",
            border_radius=styles.border_radius,
            width="100%",
            spacing="2",
            padding="0.35em",
            margin_top="1em",
        ),
        admin_sidebar_item(
            label="Benutzer",
            icon="users",
            url="/admin/users",
        ),
        admin_sidebar_item(
            label="Modelle",
            icon="atom",
            url="/avvia/admin/models",
        ),
        admin_sidebar_item(
            label="Server",
            icon="server",
            url="/avvia/admin/servers",
        ),
        admin_sidebar_item(
            label="MCP Server",
            icon="plug",
            svg="/icons/mcp.svg",
            url="/assistant/admin/mcp-servers",
        ),
        admin_sidebar_item(
            label="Nutzungsdaten",
            icon="database",
            url="/avvia/admin/import",
        ),
        width="95%",
        spacing="1",
    )


def navbar_items() -> rx.Component:
    return rx.vstack(
        rx.text("Demos", size="2", weight="bold", style=sub_heading_styles),
        requires_role(
            sidebar_item(
                label="Assistent",
                icon="bot-message-square",
                url="/assistant",
            ),
            role=ASSISTANT_ROLE.name,
        ),
        requires_role(
            sidebar_item(
                label="Bildgenerator",
                icon="image",
                url="/image-generator",
            ),
            role=IMAGE_GENERATOR_ROLE.name,
        ),
        requires_role(
            sidebar_item(
                label="Zusammenfassungen",
                icon="file-text",
                url="/summarize",
            ),
            role=ASSISTANT_ROLE.name,
        ),
        requires_role(
            sidebar_item(
                label="Anonymisierung",
                icon="square-asterisk",
                url="/anonymize",
            ),
            role=ANONYMIZER_ROLE.name,
        ),
        rx.text("Intern", size="2", weight="bold", style=sub_heading_styles),
        requires_role(
            sidebar_item(
                label="Confluence Setup",
                icon="folder-git-2",
                url="/confluence",
            ),
            role=INTERNAL_ROLE.name,
        ),
        requires_role(
            sidebar_item(
                label="CATs Kostenstelle",
                icon="clock",
                url="/admin/hours",
            ),
            role=TEAM_MANAGER_ROLE.name,
        ),
        rx.spacer(min_height="1em"),
        rx.text(
            "Avvia Intelligence",
            size="2",
            weight="bold",
            margin_top="9px",
            style=sub_heading_styles,
        ),
        requires_role(
            sidebar_item(
                label="Dashboard",
                icon="home",
                url="/avvia/dashboard",
            ),
            role=AVVIA_TENANT_ROLE.name,
        ),
        requires_role(
            sidebar_item(
                label="Projekte",
                icon="square-chevron-right",
                url="/avvia/projects",
            ),
            role=AVVIA_PROJECT_ROLE.name,
        ),
        requires_role(
            sidebar_item(
                label="Mandanten",
                icon="album",
                url="/avvia/tenants",
            ),
            role=AVVIA_TENANT_ROLE.name,
        ),
        spacing="1",
        width="95%",
        margin_top="-1em",
    )


def app_navbar() -> rx.Component:
    return navbar(
        navbar_header=navbar_header(),
        navbar_items=navbar_items(),
        navbar_admin_items=navbar_admin_items(),
        version=VERSION,
    )
