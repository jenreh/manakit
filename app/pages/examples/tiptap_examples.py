"""Mantine RichTextEditor (Tiptap) Examples Page.

Demonstrates various use cases and features of the RichTextEditor component.
"""

import reflex as rx

import manakit_mantine as mn
from manakit_user.authentication.templates import navbar_layout

from app.components.navbar import app_navbar


class TiptapState(rx.State):
    """State for Tiptap editor examples."""

    # Simple editor content
    simple_content: str = (
        "<p>This is a simple rich text editor. Try formatting some text!</p>"
    )

    # Controlled editor content
    controlled_content: str = """<h2 style="text-align: center;">Welcome to
    Mantine Rich Text Editor</h2>
<p>This editor demonstrates <strong>controlled mode</strong> where content is
synced with Reflex state.</p>
<p>You can use:</p>
<ul>
<li><strong>Bold</strong>, <em>italic</em>, <u>underline</u> formatting</li>
<li>Lists (ordered and unordered)</li>
<li><mark>Highlighted text</mark></li>
<li>Links and more!</li>
</ul>"""

    # Minimal toolbar content
    minimal_toolbar_content: str = """<p>This editor has a <strong>minimal toolbar
    </strong> with only basic formatting controls.</p>"""

    # Custom toolbar content
    custom_toolbar_content: str = """<h2>Custom Toolbar Configuration</h2>
<p>This editor demonstrates custom toolbar groups!</p>"""

    # Color picker example content
    color_content: str = """<p>Select text and use the color picker to
    <span style="color: #fa5252">change</span> <span style="color: #228be6">text</span>
    <span style="color: #40c057">colors</span>!</p>"""

    # Minimal content
    minimal_content: str = ""

    # Code example
    code_content: str = """<p>You can write code inline with <code>backticks</code>
    or use code blocks:</p>
<pre><code>def hello_world():
    print("Hello from Mantine RichTextEditor!")</code></pre>"""

    # Readonly content
    readonly_content: str = """<h3>This editor is read-only</h3>
<p>The content cannot be edited, but you can select and copy text.</p>
<p>This is useful for displaying formatted content.</p>"""

    def update_simple_content(self, html: str) -> None:
        """Update simple editor content."""
        self.simple_content = html

    def update_controlled_content(self, html: str) -> None:
        """Update controlled editor content."""
        self.controlled_content = html

    def update_minimal_toolbar_content(self, html: str) -> None:
        """Update minimal toolbar editor content."""
        self.minimal_toolbar_content = html

    def update_custom_toolbar_content(self, html: str) -> None:
        """Update custom toolbar editor content."""
        self.custom_toolbar_content = html

    def update_color_content(self, html: str) -> None:
        """Update color editor content."""
        self.color_content = html

    def update_minimal_content(self, html: str) -> None:
        """Update minimal editor content."""
        self.minimal_content = html

    def reset_content(self) -> None:
        """Reset all editors to default content."""
        self.simple_content = "<p>Content has been reset!</p>"
        self.controlled_content = "<p>Content has been reset!</p>"
        self.minimal_toolbar_content = "<p>Content has been reset!</p>"
        self.custom_toolbar_content = "<p>Content has been reset!</p>"
        self.color_content = "<p>Content has been reset!</p>"
        self.minimal_content = ""


@navbar_layout(
    route="/tiptap",
    title="Rich Select Examples",
    navbar=app_navbar(),
    with_header=False,
)
def tiptap_page() -> rx.Component:
    """Main Tiptap examples page."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Mantine RichTextEditor (Tiptap)", size="9"),
            rx.text(
                "Comprehensive WYSIWYG editor based on Tiptap with full "
                "formatting support.",
                size="4",
                color_scheme="gray",
            ),
            rx.link(
                "← Back to Home",
                href="/",
                size="3",
            ),
            # Simple editor with default toolbar
            rx.heading("Rich Text Editor", size="7", mt="6"),
            rx.text(
                "Full-featured editor with pre-configured toolbar, min/max "
                "height, and sticky toolbar.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content=TiptapState.simple_content,
                on_update=TiptapState.update_simple_content,
                placeholder="Start typing...",
                sticky_toolbar=True,
                sticky_offset="0px",
                styles={"content": {"minHeight": "100px", "maxHeight": "160px"}},
                width="100%",
            ),
            rx.text(
                "Current content length: "
                + rx.cond(
                    TiptapState.simple_content,
                    TiptapState.simple_content.length().to(str),
                    "0",
                ),
                size="2",
                color_scheme="gray",
                mt="2",
            ),
            # Minimal toolbar example
            rx.heading("Minimal Toolbar", size="7", mt="8"),
            rx.text(
                "Custom toolbar with only basic formatting controls.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content=TiptapState.minimal_toolbar_content,
                on_update=TiptapState.update_minimal_toolbar_content,
                placeholder="Type with minimal toolbar...",
                toolbar_config=mn.EditorToolbarConfig(
                    control_groups=[
                        mn.ToolbarControlGroup.BASIC_FORMATTING.value,
                        mn.ToolbarControlGroup.HISTORY.value,
                    ]
                ),
                width="100%",
            ),
            # Custom toolbar example
            rx.heading("Custom Toolbar Groups", size="7", mt="8"),
            rx.text(
                "Fully custom toolbar configuration with specific controls.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content=TiptapState.custom_toolbar_content,
                on_update=TiptapState.update_custom_toolbar_content,
                placeholder="Custom toolbar example...",
                toolbar_config=mn.EditorToolbarConfig(
                    control_groups=[
                        ["bold", "italic", "underline"],
                        ["h1", "h2", "h3"],
                        ["bulletList", "orderedList"],
                        ["link", "unlink"],
                        ["image"],
                    ]
                ),
                width="100%",
            ),
            # Controlled editor with custom toolbar
            rx.heading("Controlled Editor with State", size="7", mt="8"),
            rx.text(
                "Editor content synced with Reflex state via on_update callback.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content=TiptapState.controlled_content,
                on_update=TiptapState.update_controlled_content,
                placeholder="Start typing...",
                width="100%",
            ),
            # Color picker example
            rx.heading("Text Color Support", size="7", mt="8"),
            rx.text(
                "Select text and apply colors using the color picker or preset colors.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content=TiptapState.color_content,
                on_update=TiptapState.update_color_content,
                placeholder="Select text and change its color...",
                toolbar_config=mn.EditorToolbarConfig(
                    control_groups=[
                        mn.ToolbarControlGroup.BASIC_FORMATTING.value,
                        mn.ToolbarControlGroup.COLORS.value,
                        mn.ToolbarControlGroup.HISTORY.value,
                    ]
                ),
                width="100%",
            ),
            # Minimal editor (no toolbar)
            rx.heading("Content Area", size="7", mt="8"),
            rx.text(
                "The editor automatically includes a full toolbar with all controls.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content=TiptapState.minimal_content,
                on_update=TiptapState.update_minimal_content,
                placeholder="Try Cmd+B for bold, Cmd+I for italic...",
                width="100%",
            ),
            # Code and special formatting
            rx.heading("Code Support", size="7", mt="8"),
            rx.text(
                "Inline code and code blocks with syntax highlighting.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content=TiptapState.code_content,
                placeholder="Write some code...",
                width="100%",
            ),
            # Readonly editor
            rx.heading("Read-Only Editor", size="7", mt="8"),
            rx.text(
                "Content display mode - no editing allowed.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content=TiptapState.readonly_content,
                editable=False,
                width="100%",
            ),
            # Text alignment example
            rx.heading("Text Alignment", size="7", mt="8"),
            rx.text(
                "Align paragraphs left, center, right, or justify.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content="""<h2 style="text-align: left;">Left Aligned Heading</h2>
<p style="text-align: left;">This paragraph is aligned to the left.</p>
<h2 style="text-align: center;">Center Aligned Heading</h2>
<p style="text-align: center;">This paragraph is centered.</p>
<h2 style="text-align: right;">Right Aligned Heading</h2>
<p style="text-align: right;">This paragraph is aligned to the right.</p>""",
                width="100%",
            ),
            # Subscript and superscript
            rx.heading("Subscript & Superscript", size="7", mt="8"),
            rx.text(
                "Useful for mathematical formulas and footnotes.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content="""<p>Chemical formula: H<sub>2</sub>O</p>
<p>Mathematical expression: E = mc<sup>2</sup></p>
<p>Footnote reference<sup>1</sup></p>""",
                width="100%",
            ),
            # Variant example - subtle
            rx.heading("Subtle Variant", size="7", mt="8"),
            rx.text(
                "Borderless design with larger controls and reduced spacing.",
                size="3",
                color_scheme="gray",
                mb="3",
            ),
            mn.rich_text_editor(
                content="<p>This editor uses the subtle variant style.</p>",
                variant="subtle",
                width="100%",
            ),
            # Action buttons
            rx.hstack(
                rx.button(
                    "Reset All Content",
                    on_click=TiptapState.reset_content,
                    color_scheme="red",
                    variant="outline",
                ),
                mt="6",
                mb="6",
            ),
            # Usage notes
            rx.heading("Usage Notes", size="6", mt="6"),
            rx.unordered_list(
                rx.list_item(
                    "Use ",
                    rx.code("mn.rich_text_editor()"),
                    " - all-in-one component with full toolbar",
                ),
                rx.list_item(
                    "Handles Tiptap editor lifecycle automatically via inline wrapper",
                ),
                rx.list_item(
                    "Content is HTML - use ",
                    rx.code("on_update"),
                    " event to sync with state",
                ),
                rx.list_item(
                    "Set ",
                    rx.code("editable=False"),
                    " for read-only display mode",
                ),
                rx.list_item(
                    "All extensions included: Highlight, TextAlign, Color, "
                    "Link, Subscript, Superscript, Code, and more",
                ),
                rx.list_item(
                    "Keyboard shortcuts work automatically (Cmd+B, Cmd+I, etc.)",
                ),
                size="3",
                spacing="2",
            ),
            # Technical details
            rx.heading("Technical Details", size="6", mt="6"),
            rx.text(
                "Pure Python implementation - no external JavaScript files needed.",
                size="3",
            ),
            rx.unordered_list(
                rx.list_item(
                    "Wrapper component defined inline via ",
                    rx.code("_get_custom_code()"),
                ),
                rx.list_item(
                    "Handles ",
                    rx.code("useEditor"),
                    " React hook internally with ",
                    rx.code("React.createElement"),
                ),
                rx.list_item(
                    "Syncs content bidirectionally between Reflex state "
                    "and Tiptap editor",
                ),
                rx.list_item(
                    "Based on Tiptap 2.x with Mantine UI components",
                ),
                size="3",
                spacing="2",
            ),
            spacing="4",
            width="100%",
            max_width="900px",
            padding="4",
        ),
        size="3",
        width="100%",
    )
