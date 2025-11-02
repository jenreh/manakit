"""Examples demonstrating AutoScroll and AutoScrollWithControls usage.

This page shows both components with streaming/dynamic content scenarios
to demonstrate auto-scroll and manual scroll button behaviors.
"""

from __future__ import annotations

import reflex as rx

import manakit_mantine as mn
from manakit_user.authentication.templates import navbar_layout

from app.components.navbar import app_navbar


class ChatStreamState(rx.State):
    """Demo state for streaming chat with auto-scroll."""

    scroll_position: dict = {"x": 0, "y": 0}
    at_top: bool = True
    at_bottom: bool = True

    messages: list[str] = [
        "User: Hello!",
        "Assistant: Hi there! How can I help?",
        "User: Tell me about Reflex.",
    ]

    @rx.event
    def add_message(self, msg: str) -> None:
        """Add a new message (simulates streaming)."""
        self.messages.append(msg)

    @rx.event
    def stream_response(self) -> None:
        """Simulate streaming response with multiple messages."""
        streaming_parts = [
            "Assistant: Reflex is a Python web framework",
            " that makes it easy to build full-stack apps.",
            " You define your UI and state in Python",
            " and it handles the rest.",
            " Pretty cool, right?",
        ]
        for part in streaming_parts:
            self.add_message(part)

    @rx.event
    def update_scroll_position(self, position: dict) -> None:
        # position is expected as {'x': number, 'y': number}
        self.scroll_position = position
        y = position.get("y", 0)
        # at top when y == 0
        self.at_top = y == 0
        # clear at_bottom when user scrolls (onBottomReached will set it)
        if y != 0:
            self.at_bottom = False


class DataStreamState(rx.State):
    """Demo state for data streaming with auto-scroll."""

    scroll_position: dict = {"x": 0, "y": 0}
    at_top: bool = True
    at_bottom: bool = True

    log_lines: list[str] = [
        "[INFO] Starting application...",
        "[INFO] Loading configuration...",
        "[DEBUG] Config loaded successfully",
    ]

    @rx.event
    def update_scroll_position(self, position: dict) -> None:
        # position is expected as {'x': number, 'y': number}
        self.scroll_position = position
        y = position.get("y", 0)
        # at top when y == 0
        self.at_top = y == 0

    @rx.event
    def add_log(self, level: str, message: str) -> None:
        """Add a log line."""
        self.log_lines.append(f"[{level}] {message}")

    @rx.event
    def simulate_processing(self) -> None:
        """Simulate background processing with logs."""
        logs = [
            ("INFO", "Processing started"),
            ("DEBUG", "Initializing components"),
            ("DEBUG", "Components initialized"),
            ("INFO", "Processing complete"),
        ]
        for level, msg in logs:
            self.add_log(level, msg)


def auto_scroll_example() -> rx.Component:
    """Basic AutoScroll example - auto-scrolls to bottom."""
    return rx.card(
        rx.vstack(
            rx.heading("AutoScroll Basic Example", size="4"),
            rx.text(
                "Content automatically scrolls to bottom when new messages arrive. "
                "Try clicking 'Add Message' to see it in action.",
                size="2",
                color="gray",
            ),
            rx.divider(),
            mn.scroll_area.auto_scroll(
                rx.foreach(
                    ChatStreamState.messages,
                    lambda msg: rx.box(
                        rx.text(msg, size="2"),
                        padding="3",
                        border_bottom="1px solid",
                        border_color=rx.color("gray", 4),
                    ),
                ),
                height="250px",
                width="100%",
                border="1px solid",
                border_color=rx.color("gray", 4),
                border_radius="md",
            ),
            rx.divider(),
            rx.hstack(
                rx.button(
                    "Add Message",
                    on_click=ChatStreamState.add_message("New message added"),
                    size="2",
                ),
                rx.button(
                    "Stream Response",
                    on_click=ChatStreamState.stream_response,
                    size="2",
                    color_scheme="blue",
                ),
                spacing="3",
            ),
            spacing="3",
            width="100%",
        ),
        padding="4",
        border_radius="md",
        width="100%",
    )


def auto_scroll_with_controls_example() -> rx.Component:
    """AutoScroll example 2."""
    return rx.card(
        rx.vstack(
            rx.heading("AutoScroll Example 2", size="4"),
            rx.text(
                f"At bottom: {DataStreamState.at_bottom}, ",
                f"at top: {DataStreamState.at_top}",
                size="2",
                color="gray",
            ),
            rx.text(
                f"Position: x={DataStreamState.scroll_position['x']}, "
                f"y={DataStreamState.scroll_position['y']}",
                size="2",
            ),
            rx.divider(),
            mn.scroll_area.auto_scroll(
                rx.foreach(
                    DataStreamState.log_lines,
                    lambda line: rx.box(
                        rx.text(line, size="2", font_family="monospace"),
                        padding="2",
                        border_bottom="1px solid",
                        border_color=rx.color("gray", 3),
                    ),
                ),
                height="300px",
                width="100%",
                border="1px solid",
                border_color=rx.color("gray", 4),
                border_radius="md",
                on_scroll_position_change=DataStreamState.update_scroll_position,
            ),
            rx.divider(),
            rx.hstack(
                rx.button(
                    "Add Log",
                    on_click=DataStreamState.add_log("INFO", "Manual log entry"),
                    size="2",
                ),
                rx.button(
                    "Simulate Processing",
                    on_click=DataStreamState.simulate_processing,
                    size="2",
                    color_scheme="blue",
                ),
                spacing="3",
            ),
            spacing="3",
            width="100%",
        ),
        padding="4",
        border_radius="md",
        width="100%",
    )


@navbar_layout(
    route="/auto-scroll",
    title="AutoScroll Examples",
    navbar=app_navbar(),
    with_header=False,
)
def auto_scroll_examples() -> rx.Component:
    """Main auto-scroll examples page."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("AutoScroll Components", size="8"),
            rx.text(
                "Demonstration of AutoScroll and AutoScrollWithControls components",
                size="3",
                color="gray",
            ),
            rx.link("← Back to Home", href="/", size="3"),
            rx.divider(),
            auto_scroll_example(),
            auto_scroll_with_controls_example(),
            spacing="6",
            width="100%",
        ),
        size="2",
    )
