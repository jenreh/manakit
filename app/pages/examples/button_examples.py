"""Examples demonstrating Mantine Button usage in Reflex.

This page shows common Button usages: basic, sizes & variants, left/right
sections, loading/disabled, and full width. It also includes a simple click
counter to demonstrate event wiring.
"""

from __future__ import annotations

import reflex as rx

import manakit_mantine as mn
from manakit_user.authentication.components.templates import navbar_layout

from app.components.navbar import app_navbar


class ButtonState(rx.State):
    clicks: int = 0

    @rx.event
    def increment(self) -> None:
        self.clicks += 1


@navbar_layout(
    route="/button",
    title="Button Examples",
    navbar=app_navbar(),
    with_header=False,
)
def button_examples() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Button Examples", size="8"),
            rx.text("Small showcase of Mantine Button wrapper", size="3", color="gray"),
            rx.link("← Back to Home", href="/", size="3"),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.heading("Basic Button", size="4"),
                        mn.button(
                            "Click me",
                            on_click=ButtonState.increment,
                            aria_label="Click me",
                        ),
                        rx.text(f"Clicks: {ButtonState.clicks}"),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Sizes & Variants", size="4"),
                        rx.hstack(
                            mn.button("XS", size="xs"),
                            mn.button("SM", size="sm"),
                            mn.button("MD", size="md"),
                            mn.button("LG", size="lg"),
                            mn.button("XL", size="xl"),
                            spacing="3",
                        ),
                        rx.hstack(
                            mn.button("Filled", variant="filled", color="blue"),
                            mn.button("Outline", variant="outline"),
                            mn.button("Light", variant="light"),
                            mn.button(
                                "Gradient",
                                variant="gradient",
                                gradient={"from": "indigo", "to": "cyan", "deg": 45},
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
                        rx.heading("Sections & Justify", size="4"),
                        mn.button("With left", left_section=rx.icon("search")),
                        mn.button("With right", right_section=rx.icon("chevron-right")),
                        mn.button(
                            "Space between",
                            left_section=rx.icon("star"),
                            right_section=rx.icon("chevron-right"),
                            justify="space-between",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Space between (demo)", size="4"),
                        mn.button(
                            "Space between example",
                            left_section=rx.icon("star"),
                            right_section=rx.icon("chevron-right"),
                            justify="space-between",
                            full_width=True,
                        ),
                        rx.text(
                            "A full-width button using justify='space-between' to "
                            "separate left/right sections."
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Loading & Disabled", size="4"),
                        mn.button("Load", loading=True, loader_props={"type": "dots"}),
                        mn.button("Disabled", disabled=True),
                        mn.button("Data-disabled", data_disabled=True),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Full width", size="4"),
                        mn.button("Full width button", full_width=True, color="teal"),
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
