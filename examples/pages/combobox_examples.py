import reflex as rx


class ComboState(rx.State):
    """State for the combobox examples."""

    value: str | None = None
    dropdown_opened: bool = False

    def set_value(self, val: str) -> None:
        """Set the selected value and close dropdown."""
        self.value = val
        self.dropdown_opened = False

    def toggle_dropdown(self) -> None:
        """Toggle the dropdown open/closed state."""
        self.dropdown_opened = not self.dropdown_opened

    def close_dropdown(self) -> None:
        """Close the dropdown."""
        self.dropdown_opened = False


def select_option_component(emoji: str, value: str, description: str) -> rx.Component:
    """Render a single option with emoji, label and description."""
    return rx.hstack(
        rx.text(emoji, font_size="20px"),
        rx.box(
            rx.text(value, font_weight=500, font_size="sm"),
            rx.text(description, opacity=0.6, font_size="xs"),
        ),
        spacing="2",
        align="center",
    )


def combobox_examples() -> rx.Component:
    """Combobox demo that mirrors the Mantine JavaScript example.

    Demonstrates combobox with custom option rendering and state management.
    """

    groceries = [
        {"emoji": "🍎", "value": "Apples", "description": "Crisp and refreshing fruit"},
        {
            "emoji": "🍌",
            "value": "Bananas",
            "description": "Naturally sweet and potassium-rich fruit",
        },
        {
            "emoji": "🥦",
            "value": "Broccoli",
            "description": "Nutrient-packed green vegetable",
        },
        {
            "emoji": "🥕",
            "value": "Carrots",
            "description": "Crunchy and vitamin-rich root vegetable",
        },
        {
            "emoji": "🍫",
            "value": "Chocolate",
            "description": "Indulgent and decadent treat",
        },
    ]

    # Build Combobox.Option children - each option renders SelectOption
    options = [
        # mn.combobox.option(
        #     select_option_component(
        #         emoji=item["emoji"],
        #         value=item["value"],
        #         description=item["description"],
        #     ),
        #     value=item["value"],
        #     key=item["value"],
        # )
        # for item in groceries
    ]

    # Helper to render the selected option in the target
    def render_selected():
        return rx.fragment(
            *[
                rx.cond(
                    ComboState.value == item["value"],
                    select_option_component(
                        emoji=item["emoji"],
                        value=item["value"],
                        description=item["description"],
                    ),
                    rx.fragment(),
                )
                for item in groceries
            ]
        )

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Combobox Examples", size="9"),
            rx.text(
                "Comprehensive examples of Combobox component",
                size="4",
                color="gray",
            ),
            rx.link(
                "← Back to Home",
                href="/",
                size="3",
            ),
            rx.card(
                rx.heading("Custom Combobox option rendering", size="5"),
                # mn.combobox(
                #     mn.combobox.target(
                #         mn.form_input(
                #             rx.cond(
                #                 ComboState.value,
                #                 render_selected(),
                #                 "Pick value",
                #             ),
                #             component="button",
                #             type="button",
                #             pointer=True,
                #             right_section=mn.combobox.chevron(),
                #             on_click=ComboState.toggle_dropdown,
                #             right_section_pointer_events="none",
                #         )
                #     ),
                #     mn.combobox.dropdown(
                #         mn.combobox.options(
                #             # *options,
                #             mn.combobox.option("None", value="1", key="none")
                #         ),
                #     ),
                #     label="Grocery",
                #     placeholder="Pick value",
                #     #                    opened=ComboState.dropdown_opened,
                #     #                    on_close=ComboState.close_dropdown,
                #     #                    on_option_submit=ComboState.set_value,
                # ),
                padding="md",
            ),
            rx.text(
                "Selected value: ",
                rx.cond(ComboState.value, ComboState.value, "None"),
            ),
            spacing="4",
            padding="lg",
        ),
    )
