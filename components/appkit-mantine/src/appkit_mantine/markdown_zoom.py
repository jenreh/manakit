"""Helper to include Mermaid zoom script for markdown preview."""

import reflex as rx


def mermaid_zoom_script() -> rx.Component:
    """Include the Mermaid SVG zoom JavaScript.

    Add this component to any page that uses markdown_preview with Mermaid diagrams
    to enable click-to-zoom functionality.

    Example:
        ```python
        import reflex as rx
        import appkit_mantine as mn


        def page() -> rx.Component:
            return rx.fragment(
                mn.mermaid_zoom_script(),  # Include zoom functionality
                mn.markdown_preview(
                    source="```mermaid\\ngraph TD\\nA-->B\\n```",
                    enable_mermaid=True,
                ),
            )
        ```
    """
    # Script path is relative to assets/ directory, must start with /
    return rx.script(src="/js/mermaid_zoom.js")
