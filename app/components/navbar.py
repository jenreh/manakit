from typing import Final

import reflex as rx

from manakit_commons.registry import service_registry
from manakit_user.authentication.backend.models import Role

from app.components.navbar_component import (
    admin_sidebar_item,
    border_radius,
    navbar,
    sidebar_item,
    sub_heading_styles,
)
from app.configuration import AppConfig

IMAGE_GENERATOR_ROLE = Role(
    name="image_generator",
    label="Bildgenerator",
    description="Berechtigung um Bilder zu generieren",
)
ASSISTANT_ROLE = Role(
    name="assistant",
    label="Assistent",
    description="Berechtigung um den Assistenten zu nutzen",
)

_config = service_registry().get(AppConfig)
VERSION: Final[str] = (
    f"{_config.version}-{_config.environment}"
    if _config.environment
    else _config.version
)


def navbar_header() -> rx.Component:
    return rx.hstack(
        rx.image("/img/logo.svg", height="48px", margin_top="1.2em", margin_left="0px"),
        rx.heading("ManaKit", size="8", margin_top="22px", margin_left="8px"),
        rx.spacer(),
        align="center",
        justify="center",
        width="100%",
        padding="0.35em",
        margin_bottom="0",
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
            url="/admin/mcp-servers",
        ),
        width="95%",
        spacing="1",
    )


def navbar_items() -> rx.Component:
    return rx.vstack(
        rx.text("Demos", size="2", weight="bold", style=sub_heading_styles),
        sidebar_item(
            label="Assistent",
            icon="bot-message-square",
            url="/assistant",
        ),
        sidebar_item(
            label="Bildgenerator",
            icon="image",
            url="/image-generator",
        ),
        rx.text("Inputs", size="2", weight="bold", style=sub_heading_styles),
        rx.list.unordered(
            rx.list.item(rx.link("Text Input", href="/inputs")),
            rx.list.item(rx.link("Password Input", href="/password")),
            rx.list.item(rx.link("Date Input", href="/date")),
            rx.list.item(rx.link("Number Input", href="/number")),
            rx.list.item(rx.link("Textarea", href="/textarea")),
            rx.list.item(rx.link("Json Input", href="/json-input")),
            rx.list.item(rx.link("Select", href="/select")),
            rx.list.item(rx.link("MultiSelect", href="/multi-select")),
            rx.list.item(rx.link("TagsInput", href="/tags-input")),
            rx.list.item(rx.link("Autocomplete", href="/autocomplete")),
            rx.list.item(rx.link("Rich Text Editor (Tiptap)", href="/tiptap")),
        ),
        rx.text("Buttons", size="2", weight="bold", style=sub_heading_styles),
        rx.list.unordered(
            rx.list.item(rx.link("Action Icon (Group demo)", href="/action-icon")),
            rx.list.item(rx.link("Button", href="/button")),
        ),
        rx.text("Others", size="2", weight="bold", style=sub_heading_styles),
        rx.list.unordered(
            rx.list.item(rx.link("Navigation Progress", href="/nprogress")),
            rx.list.item(rx.link("Nav Link", href="/nav-link")),
            rx.list.item(rx.link("Number Formatter", href="/number-formatter")),
            rx.list.item(rx.link("ScrollArea", href="/scroll-area")),
            rx.list.item(rx.link("Table", href="/table")),
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
