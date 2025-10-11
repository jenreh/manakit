"""Component for MCP server selection modal."""

import reflex as rx
from knai_assistant.backend.models import MCPServer
from knai_assistant.state.thread_state import ThreadState


def render_mcp_server_item(server: MCPServer) -> rx.Component:
    """Render a single MCP server item in the modal."""
    return rx.hstack(
        rx.switch(
            checked=ThreadState.server_selection_state.get(server.id, False),
            on_change=lambda checked: ThreadState.toggle_mcp_server_selection(
                server.id, checked
            ),
        ),
        rx.vstack(
            rx.text(server.name, font_weight="bold", size="2"),
            rx.text(server.description, size="1", color="gray"),
            spacing="1",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def tools_popover() -> rx.Component:
    """Render the tools modal popup."""
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.icon("pencil-ruler", size=18),
                rx.text(
                    ThreadState.selected_mcp_servers.length().to_string()
                    + " von "
                    + ThreadState.available_mcp_servers.length().to_string(),
                    size="1",
                ),
                variant="ghost",
                size="2",
                border_radius="4px",
            ),
        ),
        rx.popover.content(
            rx.vstack(
                rx.text("Werkzeuge verwalten", size="3", font_weight="bold"),
                rx.cond(
                    ThreadState.available_mcp_servers.length() > 0,
                    rx.text(
                        "Wähle die Werkzeuge aus, die für diese Unterhaltung "
                        "verfügbar sein sollen.",
                        size="2",
                        color="gray",
                        margin_bottom="1.5em",
                    ),
                    rx.text(
                        "Es sind derzeit keine Werkzeuge verfügbar. "
                        "Bitte konfigurieren Sie MCP-Server in den Einstellungen.",
                        size="2",
                        color="gray",
                        margin_top="1.5em",
                    ),
                ),
                rx.scroll_area(
                    rx.vstack(
                        rx.foreach(
                            ThreadState.available_mcp_servers,
                            render_mcp_server_item,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    width="100%",
                    max_height="210px",
                    scrollbars="vertical",
                    type="auto",
                ),
                rx.button(
                    "Anwenden",
                    on_click=ThreadState.apply_mcp_server_selection,
                    variant="solid",
                    color_scheme="blue",
                    margin_top="1.5em",
                ),
                spacing="1",
            ),
            width="400px",
            padding="1.5em",
            align="end",
            side="top",
        ),
        open=ThreadState.show_tools_modal,
        on_open_change=ThreadState.set_show_tools_modal,
        placement="bottom-start",
    )
