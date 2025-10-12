"""Examples demonstrating Mantine Combobox usage in Reflex.

This page shows comprehensive Combobox usages: basic select, searchable,
custom targets, different sizes, and various configurations. The Combobox
component uses a store-based architecture instead of React hooks.
"""

from __future__ import annotations

import reflex as rx

import manakit_mantine as mn


class ComboboxState(rx.State):
    """State used by the Combobox example pages."""

    # Basic examples
    basic_value: str = ""
    searchable_value: str = ""
    custom_target_value: str = ""

    # Advanced examples
    size_example: str = ""
    disabled_example: str = ""
    with_clear_button: str = ""

    # Multi-select example (if supported)
    multi_values: list[str] = []

    def set_basic_value(self, value: str) -> None:
        self.basic_value = value

    def set_searchable_value(self, value: str) -> None:
        self.searchable_value = value

    def set_custom_target_value(self, value: str) -> None:
        self.custom_target_value = value

    def set_size_example(self, value: str) -> None:
        self.size_example = value

    def set_disabled_example(self, value: str) -> None:
        self.disabled_example = value

    def set_with_clear_button(self, value: str) -> None:
        self.with_clear_button = value

    def clear_with_clear_button(self) -> None:
        self.with_clear_button = ""

    def set_multi_values(self, values: list[str]) -> None:
        self.multi_values = values


def combobox_examples() -> rx.Component:
    """Return a page containing comprehensive Combobox demos.

    Demos included:
    - Basic combobox with button target
    - Searchable combobox with input
    - Custom target examples
    - Different sizes and variants
    - Disabled state
    - With clear button
    - Custom dropdown content
    """

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Combobox Examples", size="8"),
            rx.text(
                "Comprehensive showcase of Mantine Combobox wrapper "
                "with store-based architecture",
                size="3",
                color="gray",
            ),
            rx.link("← Back to Home", href="/", size="3"),
            rx.divider(),
            # Basic Combobox Example
            rx.card(
                rx.vstack(
                    rx.heading("Basic Combobox", size="4"),
                    rx.text(
                        "A simple combobox with button target and predefined options.",
                        size="2",
                        color="gray.600",
                        margin_bottom="1rem",
                    ),
                    mn.combobox(
                        mn.combobox.target(
                            mn.button(
                                rx.cond(
                                    ComboboxState.basic_value,
                                    ComboboxState.basic_value,
                                    "Select fruit",
                                ),
                                mn.combobox.chevron(),
                                variant="outline",
                            )
                        ),
                        mn.combobox.dropdown(
                            mn.combobox.options(
                                mn.combobox.option("Apple", value="apple"),
                                mn.combobox.option("Banana", value="banana"),
                                mn.combobox.option("Cherry", value="cherry"),
                                mn.combobox.option("Date", value="date"),
                                mn.combobox.option("Elderberry", value="elderberry"),
                            )
                        ),
                        store="basic-combobox",
                        on_option_submit=ComboboxState.set_basic_value,
                    ),
                    rx.text(
                        f"Selected: {ComboboxState.basic_value}",
                        size="2",
                        font_weight="medium",
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="4",
                border_radius="md",
                margin_bottom="4",
            ),
            #             # Searchable Combobox Example
            #             rx.card(
            #                 rx.vstack(
            #                     rx.heading("Searchable Combobox", size="4"),
            #                     rx.text(
            #                         "Combobox with search functionality. Type to filter options.",
            #                         size="2",
            #                         color="gray.600",
            #                         margin_bottom="1rem",
            #                     ),
            #                     mn.combobox(
            #                         mn.combobox.target(
            #                             mn.button(
            #                                 rx.cond(
            #                                     ComboboxState.searchable_value,
            #                                     ComboboxState.searchable_value,
            #                                     "Search fruits...",
            #                                 ),
            #                                 mn.combobox.chevron(),
            #                                 variant="outline",
            #                             )
            #                         ),
            #                         mn.combobox.dropdown(
            #                             mn.combobox.search(
            #                                 placeholder="Search fruits...",
            #                                 value=ComboboxState.searchable_value,
            #                                 on_change=ComboboxState.set_searchable_value,
            #                             ),
            #                             mn.combobox.options(
            #                                 mn.combobox.option("Apple", value="apple"),
            #                                 mn.combobox.option("Banana", value="banana"),
            #                                 mn.combobox.option("Cherry", value="cherry"),
            #                                 mn.combobox.option("Date", value="date"),
            #                                 mn.combobox.option("Elderberry", value="elderberry"),
            #                                 mn.combobox.option("Fig", value="fig"),
            #                                 mn.combobox.option("Grape", value="grape"),
            #                             ),
            #                             mn.combobox.empty(
            #                                 rx.text("No fruits found", color="gray.500")
            #                             ),
            #                         ),
            #                         # store="searchable-combobox",
            #                         on_option_submit=ComboboxState.set_searchable_value,
            #                     ),
            #                     rx.text(
            #                         f"Selected: {ComboboxState.searchable_value}",
            #                         size="2",
            #                         font_weight="medium",
            #                     ),
            #                     spacing="3",
            #                     width="100%",
            #                 ),
            #                 padding="4",
            #                 border_radius="md",
            #                 margin_bottom="4",
            #             ),
            #             # Custom Target with Input
            #             rx.card(
            #                 rx.vstack(
            #                     rx.heading("Custom Target with Input", size="4"),
            #                     rx.text(
            #                         "Combobox with a custom input target instead of a button.",
            #                         size="2",
            #                         color="gray.600",
            #                         margin_bottom="1rem",
            #                     ),
            #                     mn.combobox(
            #                         mn.combobox.target(
            #                             mn.form_input(
            #                                 placeholder="Select or type...",
            #                                 value=ComboboxState.custom_target_value,
            #                                 on_change=ComboboxState.set_custom_target_value,
            #                             )
            #                         ),
            #                         mn.combobox.dropdown(
            #                             mn.combobox.options(
            #                                 mn.combobox.option("Option 1", value="opt1"),
            #                                 mn.combobox.option("Option 2", value="opt2"),
            #                                 mn.combobox.option("Option 3", value="opt3"),
            #                                 mn.combobox.option("Custom Value", value="custom"),
            #                             )
            #                         ),
            #                         # store="custom-target-combobox",
            #                         on_option_submit=ComboboxState.set_custom_target_value,
            #                     ),
            #                     rx.text(
            #                         f"Selected: {ComboboxState.custom_target_value}",
            #                         size="2",
            #                         font_weight="medium",
            #                     ),
            #                     spacing="3",
            #                     width="100%",
            #                 ),
            #                 padding="4",
            #                 border_radius="md",
            #                 margin_bottom="4",
            #             ),
            #             # Sizes and Variants
            #             rx.card(
            #                 rx.vstack(
            #                     rx.heading("Sizes and Variants", size="4"),
            #                     rx.text(
            #                         "Combobox in different sizes and configurations.",
            #                         size="2",
            #                         color="gray.600",
            #                         margin_bottom="1rem",
            #                     ),
            #                     rx.hstack(
            #                         mn.combobox(
            #                             mn.combobox.target(
            #                                 mn.button(
            #                                     rx.cond(
            #                                         ComboboxState.size_example,
            #                                         ComboboxState.size_example,
            #                                         "XS",
            #                                     ),
            #                                     mn.combobox.chevron(),
            #                                     variant="outline",
            #                                 )
            #                             ),
            #                             mn.combobox.dropdown(
            #                                 mn.combobox.options(
            #                                     mn.combobox.option("Small", value="small"),
            #                                     mn.combobox.option("Medium", value="medium"),
            #                                     mn.combobox.option("Large", value="large"),
            #                                 )
            #                             ),
            #                             # store="size-xs-combobox",
            #                             on_option_submit=ComboboxState.set_size_example,
            #                         ),
            #                         mn.combobox(
            #                             mn.combobox.target(
            #                                 mn.button(
            #                                     rx.cond(
            #                                         ComboboxState.size_example,
            #                                         ComboboxState.size_example,
            #                                         "MD",
            #                                     ),
            #                                     mn.combobox.chevron(),
            #                                     size="3",
            #                                     variant="filled",
            #                                 )
            #                             ),
            #                             mn.combobox.dropdown(
            #                                 mn.combobox.options(
            #                                     mn.combobox.option("Small", value="small"),
            #                                     mn.combobox.option("Medium", value="medium"),
            #                                     mn.combobox.option("Large", value="large"),
            #                                 )
            #                             ),
            #                             # store="size-md-combobox",
            #                             on_option_submit=ComboboxState.set_size_example,
            #                         ),
            #                         spacing="3",
            #                     ),
            #                     rx.text(
            #                         f"Selected: {ComboboxState.size_example}",
            #                         size="2",
            #                         font_weight="medium",
            #                     ),
            #                     spacing="3",
            #                     width="100%",
            #                 ),
            #                 padding="4",
            #                 border_radius="md",
            #                 margin_bottom="4",
            #             ),
            #             # With Clear Button
            #             rx.card(
            #                 rx.vstack(
            #                     rx.heading("With Clear Button", size="4"),
            #                     rx.text(
            #                         "Combobox with a clear button to reset the selection.",
            #                         size="2",
            #                         color="gray.600",
            #                         margin_bottom="1rem",
            #                     ),
            #                     mn.combobox(
            #                         mn.combobox.target(
            #                             rx.hstack(
            #                                 mn.form_input(
            #                                     placeholder="Select option...",
            #                                     value=ComboboxState.with_clear_button,
            #                                     on_change=ComboboxState.set_with_clear_button,
            #                                     # right_section=mn.combobox.clear_button(),
            #                                 ),
            #                                 spacing="0",
            #                             )
            #                         ),
            #                         mn.combobox.dropdown(
            #                             mn.combobox.options(
            #                                 mn.combobox.option("Clearable Option 1", value="opt1"),
            #                                 mn.combobox.option("Clearable Option 2", value="opt2"),
            #                                 mn.combobox.option("Clearable Option 3", value="opt3"),
            #                             )
            #                         ),
            #                         # store="clear-button-combobox",
            #                         on_option_submit=ComboboxState.set_with_clear_button,
            #                     ),
            #                     rx.text(
            #                         f"Selected: {ComboboxState.with_clear_button}",
            #                         size="2",
            #                         font_weight="medium",
            #                     ),
            #                     spacing="3",
            #                     width="100%",
            #                 ),
            #                 padding="4",
            #                 border_radius="md",
            #                 margin_bottom="4",
            #             ),
            #             # Custom Dropdown Content
            #             rx.card(
            #                 rx.vstack(
            #                     rx.heading("Custom Dropdown Content", size="4"),
            #                     rx.text(
            #                         "Combobox with custom dropdown content "
            #                         "including headers and dividers.",
            #                         size="2",
            #                         color="gray.600",
            #                         margin_bottom="1rem",
            #                     ),
            #                     mn.combobox(
            #                         mn.combobox.target(
            #                             mn.button(
            #                                 rx.cond(
            #                                     ComboboxState.basic_value,
            #                                     ComboboxState.basic_value,
            #                                     "Select category",
            #                                 ),
            #                                 mn.combobox.chevron(),
            #                                 variant="outline",
            #                             )
            #                         ),
            #                         mn.combobox.dropdown(
            #                             rx.vstack(
            #                                 rx.text(
            #                                     "Fruits",
            #                                     size="2",
            #                                     font_weight="bold",
            #                                     padding="2",
            #                                 ),
            #                                 mn.combobox.options(
            #                                     mn.combobox.option("Apple", value="apple"),
            #                                     mn.combobox.option("Banana", value="banana"),
            #                                     mn.combobox.option("Cherry", value="cherry"),
            #                                 ),
            #                                 rx.divider(),
            #                                 rx.text(
            #                                     "Vegetables",
            #                                     size="2",
            #                                     font_weight="bold",
            #                                     padding="2",
            #                                 ),
            #                                 mn.combobox.options(
            #                                     mn.combobox.option("Carrot", value="carrot"),
            #                                     mn.combobox.option("Broccoli", value="broccoli"),
            #                                     mn.combobox.option("Spinach", value="spinach"),
            #                                 ),
            #                                 spacing="0",
            #                             )
            #                         ),
            #                         # store="custom-dropdown-combobox",
            #                         on_option_submit=ComboboxState.set_basic_value,
            #                     ),
            #                     rx.text(
            #                         f"Selected: {ComboboxState.basic_value}",
            #                         size="2",
            #                         font_weight="medium",
            #                     ),
            #                     spacing="3",
            #                     width="100%",
            #                 ),
            #                 padding="4",
            #                 border_radius="md",
            #                 margin_bottom="4",
            #             ),
            #             # State Display
            #             rx.card(
            #                 rx.vstack(
            #                     rx.heading("Current State", size="4"),
            #                     rx.code_block(
            #                         f"""Basic: {ComboboxState.basic_value}
            # Searchable: {ComboboxState.searchable_value}
            # Custom Target: {ComboboxState.custom_target_value}
            # Size Example: {ComboboxState.size_example}
            # With Clear Button: {ComboboxState.with_clear_button}""",
            #                         language="markdown",
            #                     ),
            #                     spacing="3",
            #                     width="100%",
            #                 ),
            #                 padding="4",
            #                 border_radius="md",
            #             ),
            spacing="4",
            width="100%",
            max_width="800px",
            margin="0 auto",
        ),
    )
