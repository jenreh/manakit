from __future__ import annotations

from typing import Final, Literal

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

from appkit_mantine.base import MantineInputComponentBase

IMASK_VERSION: str = "7.6.1"


class MaskedInput(MantineInputComponentBase):
    """Mantine InputBase with IMask integration for masked input fields.

    This component combines Mantine's InputBase with react-imask for automatic
    input formatting. It inherits all common input props from MantineInputComponentBase
    (label, description, error, sections, etc.) and adds IMask-specific configuration.

    Based on: https://imask.js.org/guide.html

    IMPORTANT: This is an UNCONTROLLED component!
    - DO NOT use 'value' prop (it prevents typing)
    - Use 'on_accept' to capture formatted values
    - Use 'default_value' for initial values only

    Inherits from MantineInputComponentBase:
    - Input.Wrapper props (label, description, error, required, with_asterisk)
    - Visual variants (variant, size, radius)
    - State props (default_value, placeholder, disabled, read_only)
    - HTML attributes (name, id, aria_label, max_length, pattern, etc.)
    - Section props (left_section, right_section with widths and pointer_events)
    - Mantine style props (w, maw, m, mt, mb, ml, mr, mx, my, p, etc.)
    - Event handlers (on_focus, on_blur, on_key_down, on_key_up)

    Example:
        ```python
        import reflex as rx
        from appkit_mantine import masked_input


        class State(rx.State):
            phone: str = ""

            def handle_phone(self, value: str) -> None:
                self.phone = value


        # Phone number input - CORRECT USAGE
        masked_input(
            mask="+1 (000) 000-0000",
            label="Your phone",
            placeholder="Your phone",
            on_accept=State.handle_phone,  # ✅ Capture value here
            # value=State.phone,  # ❌ DO NOT USE - prevents typing!
        )

        # Credit card input with icon
        masked_input(
            mask="0000 0000 0000 0000",
            label="Card number",
            placeholder="Card number",
            left_section=rx.icon("credit-card"),
            left_section_pointer_events="none",
            on_accept=State.handle_card,
        )

        # Date input
        masked_input(
            mask="00/00/0000",
            label="Date",
            placeholder="MM/DD/YYYY",
            description="Enter date in MM/DD/YYYY format",
            left_section=rx.icon("calendar"),
            on_accept=State.handle_date,
        )

        # With initial value
        masked_input(
            mask="+1 (000) 000-0000",
            label="Phone",
            default_value="+1 (555) 123-4567",  # ✅ Use default_value
            on_accept=State.handle_phone,
        )

        # With validation
        masked_input(
            mask="+1 (000) 000-0000",
            label="Phone",
            required=True,
            with_asterisk=True,
            error=State.phone_error,
            on_accept=State.handle_phone,
        )
        ```
    """

    tag = "InputBase"
    lib_dependencies: list[str] = [f"react-imask@{IMASK_VERSION}"]

    def _get_custom_code(self) -> str:
        return """import '@mantine/core/styles.css';
import { IMaskInput } from 'react-imask';"""

    # Extend base _rename_props with IMask-specific camelCase conversions
    _rename_props = {
        **MantineInputComponentBase._rename_props,  # noqa: SLF001
        "placeholder_char": "placeholderChar",
    }

    # ========================================================================
    # Component Configuration
    # ========================================================================

    component: Final[Var[rx.Var]] = rx.Var(
        "IMaskInput"
    )  # read-only: ensures IMaskInput is used and should never be reassigned

    # ========================================================================
    # IMask-Specific Props - Only props unique to masked input
    # ========================================================================

    mask: Var[str] = None
    """Mask pattern (e.g., '+1 (000) 000-0000', '0000 0000 0000 0000')."""

    definitions: Var[dict] = None
    """Custom pattern definitions for mask characters."""

    blocks: Var[dict] = None
    """Block-based mask configuration for complex patterns."""

    lazy: Var[bool] = None
    """Show placeholder before typing (default: True)."""

    placeholder_char: Var[str] = None
    """Character for placeholder (default: '_')."""

    overwrite: Var[bool] = None
    """Allow overwriting characters (default: False)."""

    autofix: Var[bool] = None
    """Auto-fix input on blur (default: False)."""

    eager: Var[bool] = None
    """Eager mode for immediate mask display."""

    unmask: Var[bool | Literal["typed"]] = None
    """Return unmasked value. True = all unmasked, 'typed' = only typed chars."""

    # ========================================================================
    # IMask-Specific Event Handlers
    # ========================================================================

    on_accept: EventHandler[rx.event.input_event]
    """Called when mask accepts input (receives value directly, not event).
    Use this instead of on_change for masked inputs."""

    on_complete: EventHandler[rx.event.input_event]
    """Called when mask is completely filled (receives value directly)."""

    # Note: on_change, on_focus, on_blur, etc. inherited from base class


# ============================================================================
# Convenience Function
# ============================================================================

masked_input = MaskedInput.create
