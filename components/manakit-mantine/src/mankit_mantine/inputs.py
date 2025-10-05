from __future__ import annotations

from typing import Any, Literal

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

from .base import MantineInputComponentBase


class Input(MantineInputComponentBase):
    """Mantine Input component - polymorphic base input element.

    The Input component is a polymorphic component that can be used to create
    custom inputs. It supports left and right sections for icons or controls,
    multiple variants, sizes, and full accessibility support.

    Note: In most cases, you should use TextInput or other specialized input
    components instead of using Input directly. Input is designed as a base
    for creating custom inputs.
    """

    tag = "Input"

    # Polymorphic component prop - can change the underlying element
    component: Var[str]

    # Visual variants
    variant: Var[Literal["default", "filled", "unstyled"]]
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]
    radius: Var[Literal["xs", "sm", "md", "lg", "xl"]]

    # State props
    disabled: Var[bool]
    error: Var[bool]
    required: Var[bool]

    # Input value and placeholder
    value: Var[str]
    default_value: Var[str]
    placeholder: Var[str]

    # HTML input attributes
    type: Var[str]  # Input type (text, email, tel, url, password, etc.)
    pattern: Var[str]  # HTML5 pattern validation
    input_mode: Var[str]  # inputMode for mobile keyboards
    auto_complete: Var[str]  # Autocomplete attribute
    max_length: Var[int]  # Maximum length
    min_length: Var[int]  # Minimum length
    name: Var[str]  # Input name attribute
    id: Var[str]  # Input id attribute
    aria_label: Var[str]  # Accessibility label

    # Left and right sections
    left_section: Var[Any]  # Accepts any React component
    right_section: Var[Any]  # Accepts any React component
    left_section_width: Var[int | str]
    right_section_width: Var[int | str]
    left_section_pointer_events: Var[str]  # CSS pointer-events: none, auto, all, etc.
    right_section_pointer_events: Var[str]  # CSS pointer-events: none, auto, all, etc.

    # Pointer props
    pointer: Var[bool]  # Changes cursor to pointer

    # Event handlers
    # on_change uses input_event to get value from event.target.value
    on_change: EventHandler[rx.event.input_event]
    on_focus: EventHandler[rx.event.no_args_event_spec]
    on_blur: EventHandler[rx.event.no_args_event_spec]
    on_key_down: EventHandler[rx.event.key_event]
    on_key_up: EventHandler[rx.event.key_event]


# ============================================================================
# Input.Wrapper Component
# ============================================================================


class InputWrapper(MantineInputComponentBase):
    """Mantine Input.Wrapper component - wraps input with label, description, and error.

    Input.Wrapper is used in all Mantine inputs under the hood to provide
    consistent layout for labels, descriptions, and error messages.

    The inputWrapperOrder prop controls the order of rendered elements:
    - label: Input label
    - input: Input element
    - description: Input description
    - error: Error message
    """

    tag = "Input.Wrapper"

    # Content
    label: Var[str]
    description: Var[str]
    error: Var[str]

    # Props
    required: Var[bool]
    with_asterisk: Var[bool]  # Shows asterisk without required attribute

    # Size and appearance
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]

    # ID for accessibility
    id: Var[str]

    # Layout control - order of elements in wrapper
    input_wrapper_order: Var[list[Literal["label", "input", "description", "error"]]]

    # Container for custom input wrapping
    input_container: Var[Any]


# ============================================================================
# Input Sub-Components
# ============================================================================


class InputLabel(MantineInputComponentBase):
    """Mantine Input.Label component - label element for inputs.

    Used to create custom form layouts when Input.Wrapper doesn't meet requirements.
    """

    tag = "Input.Label"

    # Props
    required: Var[bool]
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]
    html_for: Var[str]  # ID of associated input


class InputDescription(MantineInputComponentBase):
    """Mantine Input.Description component - description text for inputs.

    Used to create custom form layouts when Input.Wrapper doesn't meet requirements.
    """

    tag = "Input.Description"

    # Props
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]


class InputError(MantineInputComponentBase):
    """Mantine Input.Error component - error message for inputs.

    Used to create custom form layouts when Input.Wrapper doesn't meet requirements.
    """

    tag = "Input.Error"

    # Props
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]


class InputPlaceholder(MantineInputComponentBase):
    """Mantine Input.Placeholder component - placeholder for button-based inputs.

    Used to add placeholder text to Input components based on button elements
    or that don't support placeholder property natively.
    """

    tag = "Input.Placeholder"


class InputClearButton(MantineInputComponentBase):
    """Mantine Input.ClearButton component - clear button for inputs.

    Use to add a clear button to custom inputs. Size is automatically
    inherited from the input.
    """

    tag = "Input.ClearButton"

    # Props
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]

    # Event handlers
    on_click: EventHandler[rx.event.no_args_event_spec]


# ============================================================================
# Convenience Functions
# ============================================================================


class InputNamespace(rx.ComponentNamespace):
    """Namespace for Combobox components."""

    __call__ = staticmethod(Input.create)
    wrapper = staticmethod(InputWrapper.create)
    label = staticmethod(InputLabel.create)
    description = staticmethod(InputDescription.create)
    error = staticmethod(InputError.create)
    placeholder = staticmethod(InputPlaceholder.create)
    clear_button = staticmethod(InputClearButton.create)


form_input = InputNamespace()
