"""ScrollArea wrapper with built-in scroll controls and
buffer-based button visibility.

This component extends the Mantine ScrollArea with automatic
scroll-to-top/bottom buttons that only appear when the scroll
position is outside configurable buffer zones.
"""

from __future__ import annotations

import secrets
from typing import Literal

import reflex as rx

from manakit_mantine.scroll_area import scroll_area


def scroll_area_with_controls(
    *children,
    top_buffer: int = 0,
    bottom_buffer: int = 0,
    show_controls: bool = True,
    controls: Literal["top", "bottom", "top-bottom"] = "top-bottom",
    top_button_text: str = "↑ Top",
    bottom_button_text: str = "↓ Bottom",
    button_props: dict | None = None,
    height: str = "300px",
    viewport_id: str | None = None,
    # ScrollArea props
    scroll_type: Literal["auto", "scroll", "always", "hover", "never"] = "auto",
    scrollbars: Literal[False, "x", "y", "xy"] = "xy",
    scrollbar_size: str | int = "0.75rem",
    offset_scrollbars: bool | Literal["x", "y", "present"] = True,
    button_align: Literal["center", "left", "right"] = "center",
    **props,
) -> rx.Component:
    """Create a ScrollArea with integrated scroll controls and
    buffer-based button visibility.

    This component automatically manages scroll position tracking and shows/
    hides scroll buttons based on configurable buffer zones with smooth
    fade transitions.

    Args:
        *children: Content to display in the scroll area
        top_buffer: Distance in pixels from top where top button hides.
            (default: 0)
        bottom_buffer: Distance in pixels from bottom where bottom button
            hides. (default: 0)
        show_controls: Whether to show scroll control buttons.
            (default: True)
        controls: Which controls to show: "top", "bottom", or
            "top-bottom" (default: "top-bottom")
        controls_position: Where to show controls: "top", "bottom",
            or "both" (default: "bottom")
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
    if viewport_id is None:
        # Use secrets to generate a short random id
        viewport_id = f"scroll-vp-{secrets.token_hex(4)}"

    button_id_top = f"{viewport_id}-btn-top"
    button_id_bottom = f"{viewport_id}-btn-bottom"
    wrapper_id = f"{viewport_id}-wrapper"

    if button_props is None:
        button_props = {}

    # JavaScript to manage button visibility
    # Note: Mantine ScrollArea uses a viewport div that we need to target
    js_tpl = """
(function() {
    const wrapper = document.getElementById('@@WRAPPER_ID@@');
    if (!wrapper) return;

    // Inject scoped styles for the floating buttons (light/dark aware)
    if (!document.getElementById('@@WRAPPER_ID@@-manakit-scroll-styles')) {
        const style = document.createElement('style');
        style.id = '@@WRAPPER_ID@@-manakit-scroll-styles';
        style.innerHTML = `
            /* Scoped floating button styles */
            #@@WRAPPER_ID@@ .manakit-scroll-btn {
                transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
                opacity: 0;
                visibility: hidden;
                border-radius: 9999px;
                padding: 6px;
                min-width: 40px;
                height: 40px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.12);
                border: 1px solid rgba(0,0,0,0.08);
                background: rgba(255,255,255,0.95);
                color: inherit;
            }
            /* Make SVG icons inherit current color so arrows are visible */
            #@@WRAPPER_ID@@ .manakit-scroll-btn svg,
            #@@WRAPPER_ID@@ .manakit-scroll-btn svg * {
                fill: currentColor !important;
                stroke: currentColor !important;
            }
            @media (prefers-color-scheme: dark) {
                #@@WRAPPER_ID@@ .manakit-scroll-btn {
                    background: rgba(0,0,0,0.55);
                    box-shadow: 0 2px 10px rgba(0,0,0,0.6);
                    border: 1px solid rgba(255,255,255,0.06);
                    color: inherit;
                }
            }
        `;
        document.head.appendChild(style);
    }

    const viewport = wrapper.querySelector(
        '[data-radix-scroll-area-viewport]'
    ) || document.getElementById('@@VIEWPORT_ID@@');
    if (!viewport) {
        console.warn('Viewport not found for @@VIEWPORT_ID@@');
        return;
    }

    const btnTop = document.getElementById('@@BUTTON_TOP@@');
    const btnBottom = document.getElementById('@@BUTTON_BOTTOM@@');

    function updateButtons() {
        const scrollY = viewport.scrollTop;
        const scrollHeight = viewport.scrollHeight;
        const clientHeight = viewport.clientHeight;
        const maxScroll = scrollHeight - clientHeight;

        if (btnTop) {
            const shouldShowTop = scrollY > @@TOP_BUFFER@@;
            btnTop.style.opacity = shouldShowTop ? '1' : '0';
            btnTop.style.visibility = shouldShowTop ? 'visible' : 'hidden';
        }

        if (btnBottom) {
            const isNearBottom = scrollY >= (maxScroll - @@BOTTOM_BUFFER@@);
            const shouldShowBottom = !isNearBottom;
            btnBottom.style.opacity = shouldShowBottom ? '1' : '0';
            btnBottom.style.visibility = shouldShowBottom ? 'visible' : 'hidden';
        }
    }

    updateButtons();

    viewport.addEventListener('scroll', updateButtons);

    setTimeout(updateButtons, 200);
})();
"""

    control_script = (
        js_tpl.replace("@@WRAPPER_ID@@", wrapper_id)
        .replace("@@VIEWPORT_ID@@", viewport_id)
        .replace("@@BUTTON_TOP@@", button_id_top)
        .replace("@@BUTTON_BOTTOM@@", button_id_bottom)
        .replace("@@TOP_BUFFER@@", str(top_buffer))
        .replace("@@BOTTOM_BUFFER@@", str(bottom_buffer))
    )

    # Scroll scripts
    scroll_to_top_script = """
 (function() {
    const wrapper = document.getElementById('@@WRAPPER_ID@@');
    if (!wrapper) return;
    const viewport = wrapper.querySelector(
        '[data-radix-scroll-area-viewport]'
    ) || document.getElementById('@@VIEWPORT_ID@@');
    if (viewport) {
        viewport.scrollTo({ top: 0, behavior: 'smooth' });
    }
})();
""".replace("@@WRAPPER_ID@@", wrapper_id).replace("@@VIEWPORT_ID@@", viewport_id)

    scroll_to_bottom_script = """
 (function() {
    const wrapper = document.getElementById('@@WRAPPER_ID@@');
    if (!wrapper) return;
    const viewport = wrapper.querySelector(
        '[data-radix-scroll-area-viewport]'
    ) || document.getElementById('@@VIEWPORT_ID@@');
    if (viewport) {
        viewport.scrollTo({ top: viewport.scrollHeight, behavior: 'smooth' });
    }
})();
""".replace("@@WRAPPER_ID@@", wrapper_id).replace("@@VIEWPORT_ID@@", viewport_id)

    # Create the scroll area
    scroll_area_component = scroll_area(
        *children,
        height=height,
        type=scroll_type,
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

    # Default floating button appearance (can be overridden via button_props)
    base_button_style = {
        "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out",
        "opacity": "0",
        "visibility": "hidden",
        "background": "#ffffff",
        "borderRadius": "9999px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.12)",
        "border": "1px solid rgba(0,0,0,0.08)",
        "padding": "6px",
        "minWidth": "40px",
        "height": "40px",
        "display": "inline-flex",
        "alignItems": "center",
        "justifyContent": "center",
    }

    # Safely merge user provided button_props without duplicating 'style' kw
    extra_button_props = {}
    user_button_style = {}
    user_button_class = ""
    if button_props:
        extra_button_props = {
            k: v
            for k, v in button_props.items()
            if k not in ("style", "class_name", "className")
        }
        user_button_style = button_props.get("style", {}) or {}
        user_button_class = (
            button_props.get("class_name") or button_props.get("className") or ""
        )

    if show_top_button:
        merged_style = {**base_button_style, **user_button_style}
        merged_class = (user_button_class + " manakit-scroll-btn").strip()
        top_button = rx.button(
            top_button_text,
            id=button_id_top,
            on_click=rx.call_script(scroll_to_top_script),
            size="2",
            style=merged_style,
            class_name=merged_class,
            **extra_button_props,
        )

    if show_bottom_button:
        merged_style = {**base_button_style, **user_button_style}
        merged_class = (user_button_class + " manakit-scroll-btn").strip()
        bottom_button = rx.button(
            bottom_button_text,
            id=button_id_bottom,
            on_click=rx.call_script(scroll_to_bottom_script),
            size="2",
            style=merged_style,
            class_name=merged_class,
            **extra_button_props,
        )

    # Assemble overlay layout: position buttons absolutely over the viewport
    # Wrapper will be relative so absolute-positioned buttons float over
    # the scroll area.

    # Return a layout with the scroll area as the base and a separate
    # absolutely positioned overlay layer that is click-through (pointerEvents:none)
    # so clicks go to the ScrollArea; buttons within the overlay have
    # pointerEvents:auto so they remain clickable.

    # Base scroll area (interactive)
    scroll_box = rx.box(scroll_area_component, style={"width": "100%"})

    # Helper to compute horizontal position based on button_align
    def horiz_pos_for(align: str) -> dict:
        if align == "left":
            return {"left": "12px", "transform": "none"}
        if align == "right":
            return {"right": "12px", "transform": "none"}
        # center
        return {"left": "50%", "transform": "translateX(-50%)"}

    overlay_items: list[rx.Component] = []

    if top_button:
        pos = horiz_pos_for(button_align)
        style = {
            "position": "absolute",
            "top": "8px",
            **pos,
            "zIndex": "20",
            "pointerEvents": "auto",
        }
        overlay_items.append(rx.box(top_button, style=style))

    if bottom_button:
        pos = horiz_pos_for(button_align)
        style = {
            "position": "absolute",
            "bottom": "8px",
            **pos,
            "zIndex": "20",
            "pointerEvents": "auto",
        }
        overlay_items.append(rx.box(bottom_button, style=style))

    overlay_layer = rx.box(
        *overlay_items,
        style={
            "position": "absolute",
            "inset": "0",
            "pointerEvents": "none",
        },
    )

    return rx.box(
        rx.box(
            scroll_box,
            overlay_layer,
            style={"position": "relative", "width": "100%"},
        ),
        id=wrapper_id,
        on_mount=rx.call_script(control_script),
        **props,
    )
