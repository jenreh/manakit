"""Mantine Combobox examples for Reflex.

Based on: https://mantine.dev/core/combobox/

This demonstrates various Combobox patterns including:
- Basic select dropdown
- Searchable autocomplete
- Multiselect with pills
- Grouped options
- Scrollable lists
- Active options
"""

import reflex as rx
import reflex_enterprise as rxe


class ComboboxState(rx.State):
    """State for managing combobox."""

    selected_value: str = ""
    is_open: bool = False

    def toggle_dropdown(self):
        self.is_open = not self.is_open

    def select_option(self, value: str):
        self.selected_value = value
        self.is_open = False


def basic_select() -> rx.Component:
    return rx.box(
        rx.heading("Basic Select", size="5"),
        rx.text(
            "Simple dropdown with button trigger",
            size="2",
            color="gray",
            margin_bottom="1rem",
        ),
        rxe.mantine.combobox(
            rxe.mantine.combobox.target(
                rx.input(type="button"),
            ),
            rxe.mantine.combobox.dropdown(
                rxe.mantine.combobox.options(
                    rxe.mantine.combobox.option("Option 1"),
                    rxe.mantine.combobox.option("Option 2"),
                    rxe.mantine.combobox.option("Option 3"),
                ),
            ),
            label="Combobox",
            placeholder="Select a value",
        ),
        padding="1em",
    )


def combobox_examples() -> rx.Component:
    """Return a page containing multiple Combobox demos.

    Demos included (based on Mantine Combobox docs):
    - Basic select with button
    - Searchable autocomplete
    - Multiselect with pills
    - Grouped options
    - Scrollable list
    - Active option
    - Without dropdown
    """

    fruits = ["🍎 Apples", "🍌 Bananas", "🍇 Grape"]
    vegetables = ["🥦 Broccoli", "🥕 Carrots", "🥬 Lettuce"]

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Combobox Examples", size="9"),
            rx.text(
                "Comprehensive examples of Combobox component from @mantine/core",
                size="4",
                color="gray",
            ),
            rx.link(
                "← Back to Home",
                href="/",
                size="3",
            ),
            # Introduction
            rx.box(
                rx.heading("Overview", size="6", margin_bottom="1rem"),
                rx.text(
                    "Combobox provides a flexible set of components to create custom select, "
                    "multiselect, or autocomplete components with full control over rendering and logic.",
                    margin_bottom="1rem",
                ),
                rx.text("Key components:", font_weight="bold", margin_bottom="0.5rem"),
                rx.unordered_list(
                    rx.list_item("Combobox: Main wrapper component"),
                    rx.list_item("Combobox.Target: Wraps the trigger element"),
                    rx.list_item("Combobox.Dropdown: Contains the options list"),
                    rx.list_item("Combobox.Options: Container for options"),
                    rx.list_item("Combobox.Option: Individual selectable item"),
                    rx.list_item("Combobox.Group: Groups options together"),
                    padding_left="2rem",
                ),
                padding="1rem",
                background_color="gray.100",
                border_radius="md",
                margin_bottom="2rem",
            ),
            rx.grid(
                # basic_select(),
                columns="2",
                spacing="4",
            ),
            # Implementation Notes
            rx.heading(
                "Implementation Notes",
                size="6",
                margin_top="2rem",
                margin_bottom="1rem",
            ),
            rx.text("useCombobox Hook:", font_weight="bold", margin_bottom="0.5rem"),
            rx.text(
                "The useCombobox hook is automatically added by the Combobox component. "
                "It creates a 'combobox' store that you reference in callbacks like "
                "'() => combobox.toggleDropdown()'.",
                margin_bottom="1rem",
            ),
            rx.text("Event Handlers:", font_weight="bold", margin_bottom="0.5rem"),
            rx.unordered_list(
                rx.list_item("on_option_submit: Called when an option is selected"),
                rx.list_item("openDropdown/closeDropdown: Control dropdown visibility"),
                rx.list_item(
                    "updateSelectedOptionIndex: Required for searchable components"
                ),
                rx.list_item("resetSelectedOption: Reset selection on dropdown close"),
                padding_left="2rem",
                margin_bottom="1rem",
            ),
            rx.text("Split Targets:", font_weight="bold", margin_bottom="0.5rem"),
            rx.text(
                "For multiselect, use EventsTarget (for keyboard events) and DropdownTarget "
                "(for positioning) separately to handle complex interactions.",
            ),
            padding="1rem",
            background_color="blue.50",
            border_radius="md",
            margin_bottom="2rem",
            spacing="4",
            max_width="1400px",
        ),
    )
