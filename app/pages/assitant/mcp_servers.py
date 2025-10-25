"""MCP server management page."""

import reflex as rx

from manakit_assistant.components import mcp_servers_table
from manakit_ui.components.header import header
from manakit_user.authentication.components.components import requires_admin
from manakit_user.authentication.templates import authenticated

from app.components.navbar import app_navbar


@authenticated(
    route="/assistant/admin/mcp-servers",
    title="MCP Server",
    navbar=app_navbar(),
    admin_only=True,
)
def mcp_servers_page() -> rx.Component:
    """Page for managing MCP servers."""
    return requires_admin(
        rx.vstack(
            header("MCP Server"),
            mcp_servers_table(),
            width="100%",
            max_width="1200px",
            spacing="6",
        ),
    )
