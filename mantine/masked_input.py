"""React-imask integration with Mantine Input for masked input fields.

Provides IMaskInput component for phone numbers, credit cards, dates, etc.
See `mantine_imask_input()` function for detailed usage and examples.

IMPORTANT: IMask components are UNCONTROLLED - use 'on_accept', not 'value'.

Documentation: https://imask.js.org/guide.html
"""

from __future__ import annotations

from typing import Any, Literal

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var


class IMaskInput(rx.Component):
    """IMaskInput component from react-imask library.

    This component provides masked input functionality with automatic formatting
    as the user types. It can be used standalone or with Mantine's Input component.
    """

    library = "react-imask@7.6.1"
    tag = "IMaskInput"

    lib_dependencies: list[str] = ["react-imask@7.6.1"]

    # Prop aliasing for camelCase React props
    _rename_props = {"placeholder_char": "placeholderChar", "class_name": "className"}

    # Mask configuration
    mask: Var[str]  # Mask pattern (e.g., "+1 (000) 000-0000")

    # Alternative mask configurations (for complex patterns)
    definitions: Var[dict]  # Custom pattern definitions
    blocks: Var[dict]  # Block-based mask configuration

    # Mask behavior
    lazy: Var[bool]  # Show placeholder before typing (default: True)
    placeholder_char: Var[str]  # Character for placeholder (default: "_")
    overwrite: Var[bool]  # Allow overwriting (default: False)
    autofix: Var[bool]  # Auto-fix input on blur (default: False)
    eager: Var[bool]  # Eager mode for mask display

    # Input value
    value: Var[str]  # Current value
    unmask: Var[bool | Literal["typed"]]  # Return unmasked value

    # Input props (standard HTML input attributes)
    placeholder: Var[str]
    disabled: Var[bool]
    type: Var[str]
    name: Var[str]
    id: Var[str]

    # Style props
    class_name: Var[str]  # CSS class name
    style: Var[dict]

    # Event handlers
    on_accept: EventHandler[rx.event.input_event]  # Fired when mask accepts input
    on_complete: EventHandler[rx.event.input_event]  # Fired when mask is complete
    on_change: EventHandler[rx.event.input_event]  # Standard change event
    on_focus: EventHandler[rx.event.no_args_event_spec]
    on_blur: EventHandler[rx.event.no_args_event_spec]


class MantineInputBase(rx.Component):
    """Mantine InputBase component.

    Combines Input and Input.Wrapper, supports component prop for custom
    inputs. See `mantine_input_base()` function for usage examples.
    """

    library = "@mantine/core@8.2.5"
    tag = "InputBase"

    lib_dependencies: list[str] = ["react-imask@7.6.1"]

    def _get_custom_code(self) -> str:
        return """import '@mantine/core/styles.css';
import { IMaskInput } from 'react-imask';"""

    # Prop aliasing for camelCase React props
    _rename_props = {
        "placeholder_char": "placeholderChar",
        "left_section": "leftSection",
        "right_section": "rightSection",
        "left_section_width": "leftSectionWidth",
        "right_section_width": "rightSectionWidth",
        "left_section_pointer_events": "leftSectionPointerEvents",
        "right_section_pointer_events": "rightSectionPointerEvents",
        "default_value": "defaultValue",
        "with_asterisk": "withAsterisk",
        "aria_label": "aria-label",
    }

    # Component prop - can be set to IMaskInput or any other component
    component: Var[Any]

    # InputBase wrapper props
    label: Var[str]
    description: Var[str]
    error: Var[str | bool]
    required: Var[bool]
    with_asterisk: Var[bool]

    # Mask configuration (when used with IMaskInput)
    mask: Var[str]  # Mask pattern
    definitions: Var[dict]  # Custom pattern definitions
    blocks: Var[dict]  # Block-based mask configuration
    lazy: Var[bool]  # Show placeholder before typing
    placeholder_char: Var[str]  # Placeholder character (default: "_")
    overwrite: Var[bool]  # Allow overwriting
    autofix: Var[bool]  # Auto-fix on blur
    eager: Var[bool]  # Eager mode
    unmask: Var[bool | Literal["typed"]]  # Return unmasked value

    # Mantine Input props
    variant: Var[Literal["default", "filled", "unstyled"]]
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]
    radius: Var[Literal["xs", "sm", "md", "lg", "xl"]]

    # State props
    disabled: Var[bool]

    # Input value and placeholder
    value: Var[str]
    default_value: Var[str]
    placeholder: Var[str]

    # HTML input attributes
    type: Var[str]
    name: Var[str]
    id: Var[str]
    aria_label: Var[str]

    # Left and right sections
    left_section: Var[Any]
    right_section: Var[Any]
    left_section_width: Var[int | str]
    right_section_width: Var[int | str]
    left_section_pointer_events: Var[str]
    right_section_pointer_events: Var[str]

    # Pointer props
    pointer: Var[bool]

    # Event handlers
    on_accept: EventHandler[rx.event.input_event]  # IMask-specific: value accepted
    on_complete: EventHandler[rx.event.input_event]  # IMask-specific: mask complete
    on_change: EventHandler[rx.event.input_event]  # Standard change event
    on_focus: EventHandler[rx.event.no_args_event_spec]
    on_blur: EventHandler[rx.event.no_args_event_spec]
    on_key_down: EventHandler[rx.event.key_event]
    on_key_up: EventHandler[rx.event.key_event]


# ============================================================================
# Convenience Functions
# ============================================================================


def masked_input(*children, **props) -> MantineInputBase:
    """Create a Mantine InputBase with IMask functionality.

    This is a convenience wrapper that creates an InputBase component with
    IMaskInput as the component prop.

    IMPORTANT: This is an UNCONTROLLED component!
    - DO NOT use 'value' prop (prevents typing)
    - Use 'on_accept' to capture formatted values
    - Use 'default_value' for initial values only

    Args:
        *children: Child components
        **props: Component properties

    Returns:
        MantineInputBase component instance configured for IMask

    Example:
        ```python
        # Phone number input - CORRECT USAGE
        masked_input(
            mask="+1 (000) 000-0000",
            label="Your phone",
            placeholder="Your phone",
            on_accept=State.set_phone,  # ✅ Capture value here
            # value=State.phone,  # ❌ DO NOT USE - prevents typing!
        )

        # Credit card input
        masked_input(
            mask="0000 0000 0000 0000",
            label="Card number",
            placeholder="Card number",
            left_section=rx.icon("credit-card"),
            on_accept=State.set_card_number,
        )

        # Date input
        masked_input(
            mask="00/00/0000",
            label="Date",
            placeholder="MM/DD/YYYY",
            left_section=rx.icon("calendar"),
            on_accept=State.set_date,
        )

        # With initial value
        masked_input(
            mask="+1 (000) 000-0000",
            label="Phone",
            default_value="+1 (555) 123-4567",  # ✅ Use default_value
            on_accept=State.set_phone,
        )
        ```
    """
    # Inject IMaskInput as the component prop - must be JS identifier, not string
    props["component"] = rx.Var("IMaskInput")
    return MantineInputBase.create(*children, **props)
