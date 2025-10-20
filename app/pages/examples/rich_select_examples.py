import reflex as rx

import manakit_mantine as mn
from manakit_user.authentication.components.templates import navbar_layout

from app.components.navbar import app_navbar


class State(rx.State):
    value: str
    value2: str

    def set_value(self, value: str) -> None:
        self.value = value

    def set_value2(self, value: str) -> None:
        self.value2 = value


def render_option(row: dict) -> rx.Component:
    return rx.hstack(
        rx.text(row.get("emoji", ""), width="24px"),
        rx.vstack(
            rx.text(row["label"], weight="bold"),
            rx.text(row.get("description", ""), color="gray"),
            align_items="start",
            spacing="1",
        ),
        spacing="3",
    )


def render_option2(row: dict) -> rx.Component:
    return rx.hstack(
        rx.text(row.get("emoji", ""), width="24px"),
        rx.text(row["label"], weight="bold"),
        align_items="start",
        spacing="1",
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
            "value": "pear",
            "emoji": "🍐",
            "label": "Pear",
            "description": "Indulgent and decadent treat",
        },
        {
            "value": "cherry",
            "emoji": "🍒",
            "label": "Cherry",
            "description": "Indulgent and decadent treat",
        },
    ]

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("RichSelect Examples", size="9"),
            rx.text(
                "Comprehensive examples component from @mantine/core",
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
                        height="68px",
                    ),
                    rx.text("Selected: ", rx.cond(State.value, State.value, "-")),
                    width="100%",
                    spacing="3",
                ),
                rx.card(
                    mn.rich_select(
                        mn.rich_select.map(
                            data,
                            renderer=render_option2,
                        ),
                        value=State.value2,
                        on_change=State.set_value2,
                        placeholder="Pick value",
                        position="top",
                        searchable=False,
                        width="100%",
                        min_height="50px",
                        size="sm",
                        radius="lg",
                    ),
                    rx.text("Selected: ", rx.cond(State.value2, State.value2, "-")),
                    width="100%",
                    spacing="3",
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
