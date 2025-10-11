"""Dialog components for MCP server management."""

from typing import Any

import reflex as rx
from knai_assistant.backend.models import MCPServer
from knai_assistant.state.mcp_server_state import MCPServerState
from reflex.vars import var_operation, var_operation_return
from reflex.vars.base import RETURN, CustomVarOperationReturn

from manakit_ui.components.dialogs import (
    delete_dialog,
    dialog_buttons,
    dialog_header,
)
from manakit_ui.components.form_inputs import form_field, form_textarea


@var_operation
def json(obj: rx.Var, indent: int = 4) -> CustomVarOperationReturn[RETURN]:
    return var_operation_return(
        js_expression=f"JSON.stringify(JSON.parse({obj}), null, {indent})",
        var_type=Any,
    )


def mcp_server_form_fields(server: MCPServer | None = None) -> rx.Component:
    """Reusable form fields for MCP server add/update dialogs."""
    is_edit_mode = server is not None

    fields = [
        form_field(
            name="name",
            icon="server",
            label="Name",
            hint="Eindeutiger Name des MCP-Servers",
            type="text",
            placeholder="MCP-Server Name",
            default_value=server.name if is_edit_mode else "",
            required=True,
        ),
        form_field(
            name="description",
            icon="text",
            label="Beschreibung",
            hint=(
                "Kurze Beschreibung zur besseren Identifikation und Auswahl "
                "durch das Modell"
            ),
            type="text",
            placeholder="Kurzbeschreibung (optional)",
            default_value=server.description if is_edit_mode else "",
            required=False,
        ),
        form_field(
            name="url",
            icon="link",
            label="URL",
            hint="Vollständige URL des MCP-Servers (z. B. https://example.com/mcp/v1/sse)",
            type="text",
            placeholder="https://example.com/mcp/v1/sse",
            default_value=server.url if is_edit_mode else "",
            required=True,
        ),
        form_textarea(
            name="headers_json",
            icon="code",
            label="HTTP Headers",
            hint=(
                "Geben Sie die HTTP-Header im JSON-Format ein. "
                'Beispiel: {"Content-Type": "application/json", '
                '"Authorization": "Bearer token"}'
            ),
            monospace=False,
            default_value=json(server.headers) if is_edit_mode else "{}",
            height="120px",
            width="100%",
        ),
    ]

    return rx.flex(
        *fields,
        direction="column",
        spacing="1",
    )


def add_mcp_server_button() -> rx.Component:
    """Button and dialog for adding a new MCP server."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus"),
                rx.text("Neuen MCP Server anlegen", display=["none", "none", "block"]),
                size="3",
                variant="solid",
            ),
        ),
        rx.dialog.content(
            dialog_header(
                icon="server",
                title="Neuen MCP Server anlegen",
                description="Geben Sie die Details des neuen MCP Servers ein",
            ),
            rx.flex(
                rx.form.root(
                    mcp_server_form_fields(),
                    dialog_buttons("MCP Server anlegen"),
                    on_submit=MCPServerState.add_server,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            class_name="dialog",
        ),
    )


def delete_mcp_server_dialog(server: MCPServer) -> rx.Component:
    """Use the generic delete dialog component for MCP servers."""
    return delete_dialog(
        title="MCP Server löschen",
        content=server.name,
        on_click=lambda: MCPServerState.delete_server(server.id),
        icon_button=True,
        size="2",
        variant="ghost",
        color_scheme="crimson",
    )


def update_mcp_server_dialog(server: MCPServer) -> rx.Component:
    """Dialog for updating an existing MCP server."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.icon_button(
                rx.icon("square-pen", size=20),
                size="2",
                variant="ghost",
                on_click=lambda: MCPServerState.get_server(server.id),
            ),
        ),
        rx.dialog.content(
            dialog_header(
                icon="square-pen",
                title="MCP Server aktualisieren",
                description="Aktualisieren Sie die Details des MCP Servers",
            ),
            rx.flex(
                rx.form.root(
                    mcp_server_form_fields(server),
                    dialog_buttons("MCP Server aktualisieren"),
                    on_submit=MCPServerState.modify_server,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            class_name="dialog",
        ),
    )
