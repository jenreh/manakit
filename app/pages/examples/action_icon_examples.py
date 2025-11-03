"""Examples demonstrating Mantine ActionIcon usage in Reflex.

This file provides simple examples of the ActionIcon component:
- Basic ActionIcon with icon child
- Different sizes and variants
- Disabled state
- Click handler with a counter in State

"""

from __future__ import annotations

import reflex as rx

import appkit_mantine as mn
from appkit_user.authentication.templates import navbar_layout

from app.components.navbar import app_navbar


class ActionIconState(rx.State):
    """State for ActionIcon examples."""

    clicks: int = 0

    @rx.event
    def increment(self) -> None:
        self.clicks += 1


@navbar_layout(
    route="/action-icon",
    title="ActionIcon Examples",
    navbar=app_navbar(),
    with_header=False,
)
def action_icon_examples() -> rx.Component:
    """Page showing examples of `action_icon` usage."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("ActionIcon Examples", size="8"),
            rx.text(
                "Small showcase of mantine ActionIcon wrapper",
                size="3",
                color="gray",
            ),
            rx.link("← Back to Home", href="/", size="3"),
            # Examples
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.heading("Basic ActionIcon", size="4"),
                        mn.action_icon(
                            rx.icon("trash"),
                            on_click=ActionIconState.increment,
                            aria_label="Delete",
                        ),
                        rx.text(f"Clicks: {ActionIconState.clicks}"),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Sizes and Variants", size="4"),
                        rx.hstack(
                            mn.action_icon(rx.icon("star"), size="xs"),
                            mn.action_icon(rx.icon("star"), size="sm"),
                            mn.action_icon(rx.icon("star"), size="md"),
                            mn.action_icon(rx.icon("star"), size="lg"),
                            mn.action_icon(rx.icon("star"), size="xl"),
                            spacing="3",
                        ),
                        rx.hstack(
                            mn.action_icon(
                                rx.icon("heart"),
                                variant="filled",
                                color="blue",
                            ),
                            mn.action_icon(
                                rx.icon("heart"),
                                variant="light",
                                color="red",
                            ),
                            mn.action_icon(rx.icon("heart"), variant="subtle"),
                            mn.action_icon(
                                rx.icon("heart"),
                                variant="outline",
                            ),
                            mn.action_icon(
                                rx.icon("heart"),
                                variant="gradient",
                                gradient={"from": "blue", "to": "grape", "deg": 90},
                            ),
                            spacing="3",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Disabled / States", size="4"),
                        mn.action_icon(rx.icon("ban"), disabled=True),
                        mn.action_icon(
                            rx.icon("check"),
                            disabled=False,
                            color="gray",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("With Loader", size="4"),
                        mn.action_icon(
                            size="xl",
                            loading=True,
                            loader_props={"type": "dots"},
                            aria_label="Loading",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Group Example", size="4"),
                        mn.action_icon.group(
                            mn.action_icon(
                                rx.icon("arrow-left"), size="md", variant="default"
                            ),
                            mn.action_icon(
                                rx.icon("minus"), size="md", variant="default"
                            ),
                            mn.action_icon.group_section(
                                rx.text("Section"), size="md", variant="default"
                            ),
                            mn.action_icon(
                                rx.icon("arrow-right"), size="md", variant="default"
                            ),
                            orientation="horizontal",
                            spacing="2",
                            # separator=rx.divider(),
                            # separator_props={"orientation": "vertical", "size": "xs"},
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            spacing="6",
            width="100%",
            padding_y="8",
        ),
        size="3",
        width="100%",
    )
