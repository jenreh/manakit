import reflex as rx

import appkit_mantine as mn
from appkit_user.authentication.templates import navbar_layout

from app.components.navbar import app_navbar


class MultiSelectState(rx.State):
    """State used by the MultiSelect example pages.

    Each example uses its own field so they can be shown together on the page.
    """

    # Basic examples
    basic_selections: list[str] = []
    object_selections: list[str] = []
    grouped_selections: list[str] = []

    # Advanced examples
    searchable_selections: list[str] = []
    limited_selections: list[str] = []
    hidden_picked_selections: list[str] = []
    clearable_selections: list[str] = ["react"]
    check_icon_selections: list[str] = []

    def set_basic(self, value: list[str]) -> None:
        self.basic_selections = value

    def set_object(self, value: list[str]) -> None:
        self.object_selections = value

    def set_grouped(self, value: list[str]) -> None:
        self.grouped_selections = value

    def set_searchable(self, value: list[str]) -> None:
        self.searchable_selections = value

    def set_limited(self, value: list[str]) -> None:
        self.limited_selections = value

    def set_hidden_picked(self, value: list[str]) -> None:
        self.hidden_picked_selections = value

    def set_clearable(self, value: list[str]) -> None:
        self.clearable_selections = value

    def set_check_icon(self, value: list[str]) -> None:
        self.check_icon_selections = value


@navbar_layout(
    route="/multi-select",
    title="Rich Select Examples",
    navbar=app_navbar(),
    with_header=False,
)
def multi_select_examples() -> rx.Component:
    """Return a page containing multiple MultiSelect demos.

    Demos included (based on Mantine MultiSelect docs):
    - Basic usage (string data)
    - Object data (value/label objects)
    - Grouped options
    - Searchable with nothing found
    - Max values limit
    - Hide picked options
    - Clearable
    - Custom check icon positioning
    """

    # Data examples
    basic_data = ["React", "Angular", "Vue", "Svelte", "Solid"]

    object_data = [
        {"value": "react", "label": "React"},
        {"value": "angular", "label": "Angular"},
        {"value": "vue", "label": "Vue", "disabled": True},
        {"value": "svelte", "label": "Svelte"},
        {"value": "solid", "label": "Solid"},
    ]

    grouped_data = [
        {"group": "Frontend", "items": ["React", "Vue", "Svelte"]},
        {"group": "Backend", "items": ["Express", "Django", "FastAPI"]},
        {"group": "Mobile", "items": ["React Native", "Flutter"]},
    ]

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("MultiSelect Examples", size="9"),
            rx.text(
                "Comprehensive examples of MultiSelect component from @mantine/core",
                size="4",
                color="gray",
            ),
            rx.link(
                "← Back to Home",
                href="/",
                size="3",
            ),
            rx.grid(
                # Basic usage
                rx.box(
                    rx.heading("Basic Usage (string data)", size="5"),
                    mn.multi_select(
                        label="Your favorite frameworks",
                        placeholder="Pick values",
                        data=basic_data,
                        value=MultiSelectState.basic_selections,
                        on_change=MultiSelectState.set_basic,
                    ),
                    rx.text(f"Selected: {MultiSelectState.basic_selections}"),
                    padding="md",
                ),
                # Object data
                rx.box(
                    rx.heading("Object data (value/label)", size="5"),
                    mn.multi_select(
                        label="Choose frameworks",
                        placeholder="Pick values",
                        data=object_data,
                        value=MultiSelectState.object_selections,
                        on_change=MultiSelectState.set_object,
                        searchable=True,
                    ),
                    rx.text(f"Selected values: {MultiSelectState.object_selections}"),
                    padding="md",
                ),
                # Grouped options
                rx.box(
                    rx.heading("Grouped options", size="5"),
                    mn.multi_select(
                        label="Your favorite libraries",
                        placeholder="Pick values",
                        data=grouped_data,
                        value=MultiSelectState.grouped_selections,
                        on_change=MultiSelectState.set_grouped,
                        searchable=True,
                    ),
                    rx.text(f"Selected: {MultiSelectState.grouped_selections}"),
                    padding="md",
                ),
                # Searchable
                rx.box(
                    rx.heading("Searchable", size="5"),
                    mn.multi_select(
                        label="Searchable",
                        placeholder="Pick values",
                        data=[
                            *basic_data,
                            "TypeScript",
                            "JavaScript",
                            "Python",
                            "Rust",
                        ],
                        value=MultiSelectState.searchable_selections,
                        on_change=MultiSelectState.set_searchable,
                        searchable=True,
                        nothing_found_message="Nothing found...",
                    ),
                    rx.text(f"Selected: {MultiSelectState.searchable_selections}"),
                    padding="md",
                ),
                # Max values
                rx.box(
                    rx.heading("Max values (limit 2)", size="5"),
                    mn.multi_select(
                        label="Choose up to 2 frameworks",
                        placeholder="Select up to 2",
                        data=basic_data,
                        value=MultiSelectState.limited_selections,
                        on_change=MultiSelectState.set_limited,
                        max_values=2,
                    ),
                    rx.text(f"Selected: {MultiSelectState.limited_selections}"),
                    padding="md",
                ),
                # Hide picked options
                rx.box(
                    rx.heading("Hide picked options", size="5"),
                    mn.multi_select(
                        label="Your favorite libraries",
                        placeholder="Pick values",
                        data=basic_data,
                        value=MultiSelectState.hidden_picked_selections,
                        on_change=MultiSelectState.set_hidden_picked,
                        hide_picked_options=True,
                    ),
                    rx.text(f"Selected: {MultiSelectState.hidden_picked_selections}"),
                    padding="md",
                ),
                # Clearable
                rx.box(
                    rx.heading("Clearable", size="5"),
                    mn.multi_select(
                        label="Your favorite libraries",
                        placeholder="Pick values",
                        data=basic_data,
                        value=MultiSelectState.clearable_selections,
                        on_change=MultiSelectState.set_clearable,
                        clearable=True,
                        default_value=["react"],
                    ),
                    rx.text(f"Selected: {MultiSelectState.clearable_selections}"),
                    padding="md",
                ),
                # Check icon position
                rx.box(
                    rx.heading("Check icon position (right)", size="5"),
                    mn.multi_select(
                        label="Control check icon",
                        placeholder="Pick values",
                        data=basic_data,
                        value=MultiSelectState.check_icon_selections,
                        on_change=MultiSelectState.set_check_icon,
                        check_icon_position="right",
                        with_check_icon=True,
                    ),
                    rx.text(f"Selected: {MultiSelectState.check_icon_selections}"),
                    padding="md",
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
