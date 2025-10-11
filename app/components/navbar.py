from typing import Final

import reflex as rx

from manakit_commons.registry import service_registry
from manakit_user.authentication.components import requires_role

from app.components.navbar_component import (
    admin_sidebar_item,
    border_radius,
    navbar,
    sidebar_item,
    sub_heading_styles,
)
from app.configuration import AppConfig

IMAGE_GENERATOR_ROLE = rx.Role("image_generator", "Bildgenerator")
ASSISTANT_ROLE = rx.Role("assistant", "Assistent")

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
            border_radius=border_radius,
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
            label="MCP Server",
            icon="plug",
            svg="/icons/mcp.svg",
            url="/assistant/admin/mcp-servers",
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
        rx.spacer(min_height="1em"),
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
