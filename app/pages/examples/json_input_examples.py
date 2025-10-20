"""Examples for Mantine JsonInput component."""

from __future__ import annotations

import json

import reflex as rx

import manakit_mantine as mn
from manakit_user.authentication.components.templates import navbar_layout

from app.components.navbar import app_navbar


class JsonInputState(rx.State):
    value: str = ""
    error: str = ""

    @rx.event
    def set_value(self, v: str | None) -> None:
        # Ensure we always store a string to satisfy component typing
        self.value = v or ""

    @rx.event
    def validate(self) -> None:
        try:
            json.loads(self.value or "null")
            self.error = ""
        except Exception as e:
            self.error = str(e)


@navbar_layout(
    route="/json_input_examples",
    title="Input Examples",
    navbar=app_navbar(),
    with_header=False,
)
def json_input_examples() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("JsonInput Examples", size="8"),
            rx.link("← Back to Home", href="/", size="3"),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.heading("Format on blur", size="4"),
                        mn.json_input(
                            label="Your JSON",
                            placeholder="[1,2,3]",
                            validation_error="Invalid JSON",
                            default_value=JsonInputState.value,
                            on_change=JsonInputState.set_value,
                            format_on_blur=True,
                            autosize=True,
                            min_rows=3,
                            width="100%",
                        ),
                        spacing="3",
                    ),
                    padding="4",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Validation example", size="4"),
                        mn.json_input(
                            default_value=JsonInputState.value,
                            on_change=JsonInputState.set_value,
                            validation_error=JsonInputState.error,
                            placeholder="invalid json",
                            min_rows=3,
                            width="100%",
                        ),
                        rx.button("Validate", on_click=JsonInputState.validate),
                        rx.cond(
                            JsonInputState.error,
                            rx.text(JsonInputState.error, color="red"),
                            rx.fragment(),
                        ),
                        spacing="3",
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
        width="100%",
    )
