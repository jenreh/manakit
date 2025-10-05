"""Mantine NumberInput component wrapper for Reflex.

Provides numeric input with validation, formatting, and increment/decrement controls.
See `mantine_number_input()` function for detailed usage and examples.

Documentation: https://mantine.dev/core/number-input/
"""

from __future__ import annotations

from typing import Literal

from reflex.event import EventHandler
from reflex.vars.base import Var

from manakit_mantine.base import (
    MantineInputComponentBase,
)


class NumberInput(MantineInputComponentBase):
    """Mantine NumberInput component for numeric input with controls.

    Based on: https://mantine.dev/core/number-input/

    Inherits common input props from MantineInputComponentBase.
    See `mantine_number_input()` function for detailed documentation and examples.
    """

    tag = "NumberInput"
    alias = "MantineNumberInput"

    # Override value type to support numbers
    value: Var[int | float | str | None] = None
    """Controlled value (can be number or string)."""

    default_value: Var[int | float | str | None] = None
    """Uncontrolled default value."""

    # Numeric constraints
    min: Var[int | float] = None
    """Minimum allowed value."""

    max: Var[int | float] = None
    """Maximum allowed value."""

    step: Var[int | float] = None
    """Step for increment/decrement (default: 1)."""

    clamp_behavior: Var[Literal["strict", "blur", "none"]] = None
    """Value clamping behavior: strict (clamp on input), blur (clamp on blur),
    none (no clamping)."""

    # Decimal handling
    decimal_scale: Var[int] = None
    """Maximum number of decimal places."""

    fixed_decimal_scale: Var[bool] = None
    """Pad decimals with zeros to match decimal_scale."""

    decimal_separator: Var[str] = None
    """Decimal separator character (default: ".")."""

    allow_decimal: Var[bool] = None
    """Allow decimal input (default: True)."""

    # Number formatting
    allow_negative: Var[bool] = None
    """Allow negative numbers (default: True)."""

    prefix: Var[str] = None
    """Text prefix (e.g., "$")."""

    suffix: Var[str] = None
    """Text suffix (e.g., "%")."""

    thousand_separator: Var[str | bool] = None
    """Thousand separator character or True for locale default."""

    thousands_group_style: Var[Literal["thousand", "lakh", "wan", "none"]] = None
    """Grouping style: thousand (1,000,000), lakh (1,00,000), wan (1,0000),
    none (no grouping)."""

    # Controls
    hide_controls: Var[bool] = None
    """Hide increment/decrement buttons."""

    allow_mouse_wheel: Var[bool] = None
    """Allow mouse wheel to change value."""

    start_value: Var[int | float] = None
    """Value when empty input is focused (default: 0)."""

    # Override on_change to handle NumberInput's direct value (not event.target.value)
    on_change: EventHandler[lambda value: [value]] = None
    """Called when value changes (receives number or empty string directly,
    not an event object)."""


number_input = NumberInput.create
