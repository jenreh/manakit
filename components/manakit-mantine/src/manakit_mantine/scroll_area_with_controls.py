"""ScrollArea wrapper with built-in scroll controls and buffer-based button visibility.

This component extends the Mantine ScrollArea with automatic scroll-to-top/bottom buttons
that only appear when the scroll position is outside configurable buffer zones.
"""

from __future__ import annotations

from typing import Literal

import reflex as rx

from manakit_mantine.scroll_area import scroll_area


def scroll_area_with_controls(
    *children,
    top_buffer: int = 0,
    bottom_buffer: int = 0,
    show_controls: bool = True,
    controls: Literal["top", "bottom", "top-bottom"] = "top-bottom",
    controls_position: Literal["top", "bottom", "both"] = "bottom",
    top_button_text: str = "↑ Top",
    bottom_button_text: str = "↓ Bottom",
    button_props: dict | None = None,
    height: str = "300px",
    viewport_id: str | None = None,
    # ScrollArea props
    type: Literal["auto", "scroll", "always", "hover", "never"] = "auto",
    scrollbars: Literal[False, "x", "y", "xy"] = "xy",
    scrollbar_size: str | int = "0.75rem",
    offset_scrollbars: bool | Literal["x", "y", "present"] = True,
    **props,
) -> rx.Component:
    """Create a ScrollArea with integrated scroll controls and buffer-based button visibility.

    This component automatically manages scroll position tracking and shows/hides
    scroll buttons based on configurable buffer zones with smooth fade transitions.

    Args:
        *children: Content to display in the scroll area
        top_buffer: Distance in pixels from top where top button hides (default: 0)
        bottom_buffer: Distance in pixels from bottom where bottom button hides (default: 0)
        show_controls: Whether to show scroll control buttons (default: True)
        controls: Which controls to show - "top", "bottom", or "top-bottom" (default: "top-bottom")
        controls_position: Where to show controls - "top", "bottom", or "both" (default: "bottom")
        top_button_text: Text for the scroll-to-top button (default: "↑ Top")
        bottom_button_text: Text for the scroll-to-bottom button (default: "↓ Bottom")
        button_props: Additional props for buttons (default: None)
        height: Height of the scroll area (default: "300px")
        viewport_id: Custom ID for the viewport element (auto-generated if not provided)
        type: Scrollbar visibility behavior (default: "auto")
        scrollbars: Which scrollbars to show (default: "xy")
        scrollbar_size: Size of scrollbars (default: "0.75rem")
        offset_scrollbars: Whether to offset content for scrollbars (default: True)
        **props: Additional props passed to the container

    Example:
        ```python
        import reflex as rx
        from manakit_mantine import scroll_area_with_controls


        def my_page():
            return scroll_area_with_controls(
                rx.text("Long content that scrolls..."),
                height="300px",
                controls="bottom",  # Only show scroll-to-bottom button
                top_buffer=12,
                bottom_buffer=24,
            )
        ```
    """
    # Generate unique viewport ID if not provided
    import random
    import string

    if viewport_id is None:
        viewport_id = f"scroll-vp-{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"

    button_id_top = f"{viewport_id}-btn-top"
    button_id_bottom = f"{viewport_id}-btn-bottom"
    wrapper_id = f"{viewport_id}-wrapper"

    if button_props is None:
        button_props = {}

    # JavaScript to manage button visibility
    # Note: Mantine ScrollArea uses a viewport div that we need to target
    control_script = f"""
(function() {{
    const wrapper = document.getElementById('{wrapper_id}');
    if (!wrapper) return;

    // Find the Mantine viewport element (it has data-radix-scroll-area-viewport attribute)
    const viewport = wrapper.querySelector('[data-radix-scroll-area-viewport]') ||
                     document.getElementById('{viewport_id}');
    if (!viewport) {{
        console.warn('Viewport not found for {viewport_id}');
        return;
    }}

    const btnTop = document.getElementById('{button_id_top}');
    const btnBottom = document.getElementById('{button_id_bottom}');

    function updateButtons() {{
        const scrollY = viewport.scrollTop;
        const scrollHeight = viewport.scrollHeight;
        const clientHeight = viewport.clientHeight;
        const maxScroll = scrollHeight - clientHeight;

        // Show top button if scrolled past buffer (only if button exists)
        if (btnTop) {{
            const shouldShowTop = scrollY > {top_buffer};
            btnTop.style.opacity = shouldShowTop ? '1' : '0';
            btnTop.style.visibility = shouldShowTop ? 'visible' : 'hidden';
        }}

        // Show bottom button if not near bottom (only if button exists)
        if (btnBottom) {{
            const isNearBottom = scrollY >= (maxScroll - {bottom_buffer});
            const shouldShowBottom = !isNearBottom;
            btnBottom.style.opacity = shouldShowBottom ? '1' : '0';
            btnBottom.style.visibility = shouldShowBottom ? 'visible' : 'hidden';
        }}
    }}

    // Initial update
    updateButtons();

    // Update on scroll
    viewport.addEventListener('scroll', updateButtons);

    // Also update after a short delay (for content loading)
    setTimeout(updateButtons, 200);
}})();
"""

    # Scroll scripts
    scroll_to_top_script = f"""
(function() {{
    const wrapper = document.getElementById('{wrapper_id}');
    if (!wrapper) return;
    const viewport = wrapper.querySelector('[data-radix-scroll-area-viewport]') || document.getElementById('{viewport_id}');
    if (viewport) {{
        viewport.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}
}})();
"""

    scroll_to_bottom_script = f"""
(function() {{
    const wrapper = document.getElementById('{wrapper_id}');
    if (!wrapper) return;
    const viewport = wrapper.querySelector('[data-radix-scroll-area-viewport]') || document.getElementById('{viewport_id}');
    if (viewport) {{
        viewport.scrollTo({{ top: viewport.scrollHeight, behavior: 'smooth' }});
    }}
}})();
"""

    # Create the scroll area
    scroll_area_component = scroll_area(
        *children,
        height=height,
        type=type,
        scrollbars=scrollbars,
        scrollbar_size=scrollbar_size,
        offset_scrollbars=offset_scrollbars,
        viewport_props={
            "id": viewport_id,
        },
    )

    # If controls are disabled, return just the scroll area
    if not show_controls:
        return scroll_area_component

    # Create control buttons based on controls parameter
    show_top_button = controls in ["top", "top-bottom"]
    show_bottom_button = controls in ["bottom", "top-bottom"]

    top_button = None
    bottom_button = None

    if show_top_button:
        top_button = rx.button(
            top_button_text,
            id=button_id_top,
            on_click=rx.call_script(scroll_to_top_script),
            size="2",
            style={
                "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out",
                "opacity": "0",
                "visibility": "hidden",
            },
            **button_props,
        )

    if show_bottom_button:
        bottom_button = rx.button(
            bottom_button_text,
            id=button_id_bottom,
            on_click=rx.call_script(scroll_to_bottom_script),
            size="2",
            style={
                "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out",
                "opacity": "0",
                "visibility": "hidden",
            },
            **button_props,
        )

    # Assemble component based on controls_position and available buttons
    container_content = []

    if controls_position == "top":
        button_row = []
        if top_button:
            button_row.append(top_button)
        if bottom_button:
            button_row.append(bottom_button)
        if button_row:
            container_content.append(rx.hstack(*button_row, spacing="2"))
        container_content.append(scroll_area_component)
    elif controls_position == "both":
        if top_button:
            container_content.append(rx.hstack(top_button, spacing="2"))
        container_content.append(scroll_area_component)
        if bottom_button:
            container_content.append(rx.hstack(bottom_button, spacing="2"))
    else:  # bottom (default)
        container_content.append(scroll_area_component)
        button_row = []
        if top_button:
            button_row.append(top_button)
        if bottom_button:
            button_row.append(bottom_button)
        if button_row:
            container_content.append(rx.hstack(*button_row, spacing="2"))

    return rx.box(
        rx.vstack(*container_content, spacing="3", width="100%", **props),
        id=wrapper_id,
        on_mount=rx.call_script(control_script),
    )
