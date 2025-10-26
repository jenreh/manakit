"""Table component for displaying MCP servers."""

import reflex as rx
from reflex.components.radix.themes.components.table import TableRow

from manakit_assistant.backend.models import MCPServer
from manakit_assistant.components.mcp_server_dialogs import (
    add_mcp_server_button,
    delete_mcp_server_dialog,
    update_mcp_server_dialog,
)
from manakit_assistant.state.mcp_server_state import MCPServerState


def mcp_server_table_row(server: MCPServer) -> TableRow:
    """Show an MCP server in a table row."""
    return rx.table.row(
        rx.table.cell(
            server.name,
            white_space="nowrap",
        ),
        rx.table.cell(
            rx.text(
                server.description,
                title=server.description,
                style={
                    "display": "block",
                    "overflow": "hidden",
                    "text_overflow": "ellipsis",
                    "white_space": "nowrap",
                },
            ),
            white_space="nowrap",
            style={
                "max_width": "0",
                "width": "100%",
            },
        ),
        rx.table.cell(
            rx.hstack(
                update_mcp_server_dialog(server),
                delete_mcp_server_dialog(server),
                spacing="2",
                align_items="center",
            ),
            white_space="nowrap",
        ),
        justify="center",
        vertical_align="middle",
        style={"_hover": {"bg": rx.color("gray", 2)}},
    )


def mcp_servers_table() -> rx.Fragment:
    return rx.fragment(
        rx.flex(
            add_mcp_server_button(),
            rx.spacer(),
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Name", width="20%"),
                    rx.table.column_header_cell(
                        "Beschreibung", width="calc(80% - 140px)"
                    ),
                    rx.table.column_header_cell("", width="140px"),
                ),
            ),
            rx.table.body(rx.foreach(MCPServerState.servers, mcp_server_table_row)),
            size="3",
            width="100%",
            table_layout="fixed",
            on_mount=MCPServerState.load_servers_with_toast,
        ),
    )
