import reflex as rx

import manakit_mantine as mn
from manakit_user.authentication.components.templates import navbar_layout

from app.components.navbar import app_navbar


class State(rx.State):
    value: str

    def set_value(self, value: str) -> None:
        self.value = value


def render_option(row: dict) -> rx.Component:
    return rx.hstack(
        rx.text(row.get("emoji", "")),
        rx.vstack(
            rx.text(row["label"], weight="bold"),
            rx.text(row.get("description", ""), color="gray"),
            align_items="start",
            spacing="1",
        ),
        spacing="3",
    )


@navbar_layout(
    route="/rich_select",
    title="Rich Select Examples",
    navbar=app_navbar(),
    with_header=False,
)
def rich_select_example() -> rx.Component:
    data = [
        {
            "value": "apples",
            "emoji": "🍎",
            "label": "Apples",
            "description": "Crisp and refreshing fruit",
        },
        {
            "value": "bananas",
            "emoji": "🍌",
            "label": "Bananas",
            "description": "Naturally sweet and potassium-rich fruit",
        },
        {
            "value": "broccoli",
            "emoji": "🥦",
            "label": "Broccoli",
            "description": "Nutrient-packed green vegetable",
            "disabled": True,
        },
        {
            "value": "carrots",
            "emoji": "🥕",
            "label": "Carrots",
            "description": "Crunchy and vitamin-rich root vegetable",
        },
        {
            "value": "chocolate",
            "emoji": "🍫",
            "label": "Chocolate",
            "description": "Indulgent and decadent treat",
        },
    ]

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Input Examples", size="9"),
            rx.text(
                "Comprehensive examples of FormInput component from @mantine/core",
                size="4",
                color="gray",
            ),
            rx.link(
                "← Back to Home",
                href="/",
                size="3",
            ),
            rx.grid(
                rx.card(
                    mn.rich_select(
                        # Zucker-Funktion map: erzeugt Items via rx.foreach
                        mn.rich_select.map(
                            data,
                            renderer=render_option,
                        ),
                        value=State.value,
                        on_change=State.set_value,
                        searchable=True,
                        clearable=True,
                        placeholder="Pick value",
                        width="100%",
                    ),
                    rx.text("Selected: ", rx.cond(State.value, State.value, "-")),
                    width="360px",
                    height="300px",
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
    )
