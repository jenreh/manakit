from __future__ import annotations

from reflex.vars.base import Var

from .base import MANTINE_VERSION, MantineComponentBase


class NavigationProgress(MantineComponentBase):
    """Mantine NavigationProgress component - top navigation progress bar.

    Based on: https://mantine.dev/x/nprogress/

    This component renders a progress bar at the top of the page that can be
    controlled imperatively using nprogress utility functions (start, stop,
    increment, decrement, set, reset, complete).

    The component must be rendered within MantineProvider and should typically
    be placed at the root level of your application.

    Example:
        ```python
        import reflex as rx
        from mantine import navigation_progress


        def index():
            return rx.fragment(
                navigation_progress(),
                # Your app content here
            )
        ```

    Control the progress bar using custom events:
        ```python
        class State(rx.State):
            def start_loading(self):
                return rx.call_script("window.nprogress.start()")

            def complete_loading(self):
                return rx.call_script("window.nprogress.complete()")
        ```
    """

    tag = "NavigationProgress"
    library = f"@mantine/nprogress@{MANTINE_VERSION}"

    def _get_custom_code(self) -> str:
        return """import '@mantine/core/styles.css';
import '@mantine/nprogress/styles.css';
import { nprogress } from '@mantine/nprogress';

// Expose nprogress API globally for Reflex control via rx.call_script()
if (typeof window !== 'undefined') {
    window.nprogress = nprogress;
}"""

    # Color and styling
    color: Var[str] = None
    """Progress bar color (Mantine color name or CSS color)."""

    size: Var[int | str] = None
    """Progress bar height in pixels (default: 4)."""

    # Progress bar behavior
    with_transition: Var[bool] = None
    """Enable smooth transitions (default: true)."""

    step_interval: Var[int] = None
    """Auto-increment interval in milliseconds when using start()."""

    # Position
    z_index: Var[int] = None
    """CSS z-index for the progress bar (default: 9999)."""

    # Initial state
    initial_progress: Var[int] = None
    """Initial progress value (0-100)."""


# ============================================================================
# Convenience Function
# ============================================================================


navigation_progress = NavigationProgress.create
