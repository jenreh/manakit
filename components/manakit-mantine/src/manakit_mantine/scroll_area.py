"""Mantine ScrollArea components wrapper for Reflex.

Provides ScrollArea and ScrollArea.Autosize components with custom scrollbars,
scroll position tracking, and overflow detection capabilities.
See `scroll_area()` and `scroll_area_autosize()` functions for detailed usage
and examples.

Documentation: https://mantine.dev/core/scroll-area/
"""

from __future__ import annotations

from typing import Any, Literal

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

from manakit_mantine.base import MANTINE_LIBARY, MANTINE_VERSION


class ScrollArea(rx.Component):
    """Mantine ScrollArea component wrapper for Reflex.

    Based on: https://mantine.dev/core/scroll-area/

    Provides custom scrollbars with various behavior modes and scroll position
    tracking capabilities. Supports different scrollbar visibility modes and
    programmatic scroll control.

    Example:
        ```python
        import reflex as rx
        import manakit_mantine as mn


        def my_component():
            return mn.scroll_area(
                rx.text("Long content that will scroll..."),
                # More content...
                height="200px",
                type="hover",
                scrollbars="y",
                on_scroll_position_change=lambda pos: print(f"Scrolled to: {pos}"),
            )
        ```
    """

    library = f"{MANTINE_LIBARY}@{MANTINE_VERSION}"

    tag = "ScrollArea"

    def _get_custom_code(self) -> str:
        return """import '@mantine/core/styles.css';"""

    # Scrollbar behavior control
    type: Var[Literal["auto", "scroll", "always", "hover", "never"]] = "auto"
    """Defines scrollbars behavior: hover (visible on hover), scroll (visible on
    scroll), always (always visible), never (always hidden), auto (overflow auto)."""

    offset_scrollbars: Var[bool | Literal["x", "y", "present"]] = True
    """Adds padding to offset scrollbars: x (horizontal only), y (vertical only),
    xy (both), present (only when scrollbars are visible)."""

    scrollbars: Var[Literal[False, "x", "y", "xy"]] = "xy"
    """Axis at which scrollbars are rendered: x (horizontal), y (vertical),
    xy (both), false (none)."""

    # Styling and sizing
    scrollbar_size: Var[str | int] = "0.75rem"
    """Scrollbar size, any valid CSS value for width/height, numbers converted
    to rem."""

    scroll_hide_delay: Var[int] = 300
    """Delay in ms to hide scrollbars, applicable only when type is hover or scroll."""

    # Behavior
    overscroll_behavior: Var[Literal["contain", "auto", "none"]] = "auto"
    """Controls overscroll-behavior of the viewport (contain, none, auto)."""

    # Viewport control
    viewport_ref: Var[Any] = None
    """Assigns viewport element ref for programmatic scrolling."""

    viewport_props: Var[dict] = None
    """Props passed down to the viewport element."""

    # Event handlers
    on_scroll_position_change: EventHandler[lambda position: [position]] = None
    """Called with current position (x and y coordinates) when viewport is scrolled."""

    on_top_reached: EventHandler[rx.event.no_args_event_spec] = None
    """Called when scrollarea is scrolled all the way to the top."""

    on_bottom_reached: EventHandler[rx.event.no_args_event_spec] = None
    """Called when scrollarea is scrolled all the way to the bottom."""


class ScrollAreaAutosize(ScrollArea):
    """Mantine ScrollArea.Autosize component wrapper for Reflex.

    Based on: https://mantine.dev/core/scroll-area/#scrollareaautosize

    Creates scrollable containers that only show scrollbars when content exceeds
    the specified max-height. Supports overflow change detection for dynamic layouts.

    Example:
        ```python
        import reflex as rx
        import manakit_mantine as mn


        def my_component():
            return mn.scroll_area_autosize(
                rx.text("Content that may exceed max height..."),
                # Dynamic content...
                max_height="300px",
                max_width="400px",
                on_overflow_change=lambda overflow: print(
                    f"Overflow changed: {overflow}"
                ),
            )
        ```
    """

    tag = "ScrollArea.Autosize"

    # Size constraints
    mah: Var[str | int] = None
    """Maximum height - container becomes scrollable when content exceeds this
    height."""

    maw: Var[str | int] = None
    """Maximum width - container becomes scrollable when content exceeds this width."""

    # Overflow detection
    on_overflow_change: EventHandler[lambda overflow: [overflow]] = None


# ============================================================================
# Convenience Functions
# ============================================================================


class ScrollAreaNamespace(rx.ComponentNamespace):
    """Namespace factory for ScrollArea to match other component patterns."""

    __call__ = staticmethod(ScrollArea.create)
    autosize = staticmethod(ScrollAreaAutosize.create)


scroll_area = ScrollAreaNamespace()
