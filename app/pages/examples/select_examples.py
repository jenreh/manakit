import reflex as rx

import manakit_mantine as mn
from manakit_user.authentication.components.templates import navbar_layout

from app.components.navbar import app_navbar


class SelectState(rx.State):
    """State used by the Select example pages.

    Each example uses its own field so they can be shown together on the page.
    """

    simple: str = ""
    object_value: str = "py"
    multi: list[str] = []
    creatable: str = ""
    grouped: str = ""

    def set_simple(self, v: str) -> None:
        self.simple = v

    def set_object(self, v: str) -> None:
        self.object_value = v

    def set_multi(self, v) -> None:
        if isinstance(v, list):
            self.multi = v
        elif isinstance(v, str):
            if v in self.multi:
                self.multi.remove(v)
            else:
                self.multi.append(v)

    def set_creatable(self, v: str) -> None:
        self.creatable = v

    def set_grouped(self, v: str) -> None:
        self.grouped = v


@navbar_layout(
    route="/select",
    title="Input Examples",
    navbar=app_navbar(),
    with_header=False,
)
def select_examples() -> rx.Component:
    """Return a page containing multiple Select demos.

    Demos included (based on Mantine Select docs):
    - Simple (string data)
    - Object data (value/label objects)
    - Multi-select
    - Creatable
    - Grouped options
    - Searchable + clearable
    """

    # Data examples
    object_data = [
        {"value": "py", "label": "Python"},
        {"value": "js", "label": "JavaScript"},
        {"value": "rs", "label": "Rust"},
    ]

    grouped_data = [
        {"group": "Frontend", "items": ["React", "Vue", "Svelte"]},
        {"group": "Backend", "items": ["Django", "FastAPI", "Express"]},
    ]

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Select Examples", size="9"),
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
                rx.box(
                    rx.heading("Simple (string data)", size="5"),
                    mn.select(
                        label="Choose a language",
                        data=["Python", "JavaScript", "Go", "Ruby"],
                        value=SelectState.simple,
                        on_change=SelectState.set_simple,
                        placeholder="Pick one",
                    ),
                    rx.text("Selected: ", SelectState.simple),
                    padding="md",
                ),
                # Object data (value/label)
                rx.box(
                    rx.heading("Object data (value/label)", size="5"),
                    mn.select(
                        label="Choose (object)",
                        data=object_data,
                        value=SelectState.object_value,
                        on_change=SelectState.set_object,
                        searchable=True,
                        nothing_found="No matches",
                    ),
                    rx.text("Selected value: ", SelectState.object_value),
                    padding="md",
                ),
                # Creatable
                rx.box(
                    rx.heading("Clearable", size="5"),
                    mn.select(
                        label="Creatable",
                        data=["Option A", "Option B"],
                        value=SelectState.creatable,
                        on_change=SelectState.set_creatable,
                        clearable=True,
                        searchable=True,
                        placeholder="Select an option...",
                    ),
                    rx.text("Created/selected: ", SelectState.creatable),
                    padding="md",
                ),
                # Grouped
                rx.box(
                    rx.heading("Grouped options", size="5"),
                    mn.select(
                        label="Grouped",
                        data=grouped_data,
                        value=SelectState.grouped,
                        on_change=SelectState.set_grouped,
                        searchable=True,
                        nothing_found="No options",
                    ),
                    rx.text("Selected: ", SelectState.grouped),
                    padding="md",
                ),
                # Custom renderOption example
                rx.box(
                    rx.heading("Custom renderOption", size="5"),
                    # client-side JS function as a Var to customize option rendering
                    mn.select(
                        label="Select with custom option rendering",
                        placeholder="Select text align",
                        data=[
                            {"value": "left", "label": "Left"},
                            {"value": "center", "label": "Center"},
                            {"value": "right", "label": "Right"},
                            {"value": "justify", "label": "Justify"},
                        ],
                        render_option=rx.Var(
                            "( { option, checked } ) => { const icons = { left: '⬅️', center: '↔️', right: '➡️', justify: '↕️' }; return (\n  <div style={{display: 'flex', alignItems: 'center', width: '100%'}}>\n    <span style={{marginRight: 8}}>{icons[option.value]}</span>\n    <span>{option.label}</span>\n    {checked ? <span style={{marginLeft: 'auto'}}>✓</span> : null}\n  </div>\n) }",
                            _var_type=str,
                        ),
                    ),
                    padding="md",
                ),
                rx.box(
                    rx.heading("Searchable", size="5"),
                    mn.select(
                        label="Your favorite library",
                        data=[
                            "Python",
                            "JavaScript",
                            "Go",
                            "Ruby",
                            "Rust",
                            "C",
                            "C++",
                            "Java",
                        ],
                        placeholder="Pick value",
                        searchable=True,
                        clearable=True,
                        nothing_found="No matches",
                    ),
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
