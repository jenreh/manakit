import reflex as rx

import appkit_mantine as mn
from appkit_user.authentication.templates import navbar_layout

from app.components.navbar import app_navbar


class TagsInputState(rx.State):
    """State used by the TagsInput example pages.

    Each example uses its own field so they can be shown together on the page.
    """

    # Basic examples
    basic_tags: list[str] = []
    controlled_tags: list[str] = ["react", "python"]
    clearable_tags: list[str] = ["typescript"]

    # Advanced examples
    max_tags: list[str] = []
    accept_blur_tags: list[str] = []
    no_duplicates_tags: list[str] = []
    split_chars_tags: list[str] = []
    suggestions_tags: list[str] = []
    searchable_tags: list[str] = []

    def set_basic(self, value: list[str]) -> None:
        self.basic_tags = value

    def set_controlled(self, value: list[str]) -> None:
        self.controlled_tags = value

    def set_clearable(self, value: list[str]) -> None:
        self.clearable_tags = value

    def set_max_tags(self, value: list[str]) -> None:
        self.max_tags = value

    def set_accept_blur(self, value: list[str]) -> None:
        self.accept_blur_tags = value

    def set_no_duplicates(self, value: list[str]) -> None:
        self.no_duplicates_tags = value

    def set_split_chars(self, value: list[str]) -> None:
        self.split_chars_tags = value

    def set_suggestions(self, value: list[str]) -> None:
        self.suggestions_tags = value

    def set_searchable(self, value: list[str]) -> None:
        self.searchable_tags = value


@navbar_layout(
    route="/tags-input",
    title="Rich Select Examples",
    navbar=app_navbar(),
    with_header=False,
)
def tags_input_examples() -> rx.Component:
    """Return a page containing multiple TagsInput demos.

    Demos included (based on Mantine TagsInput docs):
    - Basic usage (free input)
    - Controlled component
    - Clearable
    - Max tags limit
    - Accept value on blur
    - Allow duplicates (false)
    - Split characters
    - With suggestions/data
    - Searchable
    """

    # Data examples
    tech_skills = [
        "React",
        "Vue",
        "Angular",
        "Svelte",
        "TypeScript",
        "JavaScript",
        "Python",
        "Rust",
        "Go",
        "Node.js",
    ]

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("TagsInput Examples", size="9"),
            rx.text(
                "Comprehensive examples of TagsInput component from @mantine/core",
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
                    rx.heading("Basic Usage (free input)", size="5"),
                    mn.tags_input(
                        label="Your skills",
                        placeholder="Type and press Enter",
                        value=TagsInputState.basic_tags,
                        on_change=TagsInputState.set_basic,
                    ),
                    rx.text(f"Tags: {TagsInputState.basic_tags}"),
                    padding="md",
                ),
                # Controlled
                rx.box(
                    rx.heading("Controlled component", size="5"),
                    mn.tags_input(
                        label="Favorite technologies",
                        placeholder="Add technologies",
                        value=TagsInputState.controlled_tags,
                        on_change=TagsInputState.set_controlled,
                    ),
                    rx.text(f"Tags: {TagsInputState.controlled_tags}"),
                    padding="md",
                ),
                # Clearable
                rx.box(
                    rx.heading("Clearable", size="5"),
                    mn.tags_input(
                        label="Clearable tags",
                        placeholder="Add tags",
                        value=TagsInputState.clearable_tags,
                        on_change=TagsInputState.set_clearable,
                        clearable=True,
                    ),
                    rx.text(f"Tags: {TagsInputState.clearable_tags}"),
                    padding="md",
                ),
                # Max tags
                rx.box(
                    rx.heading("Max tags (limit 3)", size="5"),
                    mn.tags_input(
                        label="Choose up to 3 skills",
                        placeholder="Add skills",
                        value=TagsInputState.max_tags,
                        on_change=TagsInputState.set_max_tags,
                        max_tags=3,
                    ),
                    rx.text(f"Tags: {TagsInputState.max_tags}"),
                    padding="md",
                ),
                # Accept on blur
                rx.box(
                    rx.heading("Accept value on blur", size="5"),
                    mn.tags_input(
                        label="Skills (blur to accept)",
                        placeholder="Type and click outside",
                        value=TagsInputState.accept_blur_tags,
                        on_change=TagsInputState.set_accept_blur,
                        accept_value_on_blur=True,
                    ),
                    rx.text(f"Tags: {TagsInputState.accept_blur_tags}"),
                    padding="md",
                ),
                # No duplicates
                rx.box(
                    rx.heading("No duplicates allowed", size="5"),
                    mn.tags_input(
                        label="Unique tags only",
                        placeholder="Try adding duplicates",
                        value=TagsInputState.no_duplicates_tags,
                        on_change=TagsInputState.set_no_duplicates,
                        allow_duplicates=False,
                    ),
                    rx.text(f"Tags: {TagsInputState.no_duplicates_tags}"),
                    padding="md",
                ),
                # Split characters
                rx.box(
                    rx.heading("Split characters (comma/space)", size="5"),
                    mn.tags_input(
                        label="Split by comma or space",
                        placeholder="Use , or space to split",
                        value=TagsInputState.split_chars_tags,
                        on_change=TagsInputState.set_split_chars,
                        split_chars=[",", " "],
                    ),
                    rx.text(f"Tags: {TagsInputState.split_chars_tags}"),
                    padding="md",
                ),
                # With suggestions
                rx.box(
                    rx.heading("With suggestions", size="5"),
                    mn.tags_input(
                        label="Tech skills",
                        placeholder="Choose or type skills",
                        data=tech_skills,
                        value=TagsInputState.suggestions_tags,
                        on_change=TagsInputState.set_suggestions,
                    ),
                    rx.text(f"Tags: {TagsInputState.suggestions_tags}"),
                    padding="md",
                ),
                # Searchable
                rx.box(
                    rx.heading("Searchable suggestions", size="5"),
                    mn.tags_input(
                        label="Search technologies",
                        placeholder="Search and select",
                        data=tech_skills,
                        value=TagsInputState.searchable_tags,
                        on_change=TagsInputState.set_searchable,
                    ),
                    rx.text(f"Tags: {TagsInputState.searchable_tags}"),
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
