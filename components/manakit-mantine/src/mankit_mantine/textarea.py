"""Mantine Textarea component wrapper for Reflex.

Provides a multiline text input with autosize support.
See `mantine_textarea()` function for detailed usage and examples.
"""

from __future__ import annotations

from typing import Literal

from reflex.vars.base import Var

from .base import (
    MantineInputComponentBase,
)


class Textarea(MantineInputComponentBase):
    """Mantine Textarea component with autosize support.

    Based on: https://mantine.dev/core/textarea/

    Inherits common input props from MantineInputComponentBase.
    See `mantine_textarea()` function for detailed documentation and examples.
    """

    tag = "Textarea"

    # HTML textarea attributes
    rows: Var[int] = None
    """Number of visible text lines (when not using autosize)."""

    cols: Var[int] = None
    """Visible width in characters."""

    wrap: Var[Literal["soft", "hard", "off"]] = None
    """Text wrapping behavior: soft (default), hard, or off."""

    # Autosize feature (uses react-textarea-autosize)
    autosize: Var[bool] = None
    """Enable automatic height adjustment based on content."""

    min_rows: Var[int] = None
    """Minimum number of rows when using autosize."""

    max_rows: Var[int] = None
    """Maximum number of rows when using autosize."""

    # Resize control
    resize: Var[Literal["none", "vertical", "both", "horizontal"]] = None
    """CSS resize property to control manual resizing."""


# ============================================================================
# Convenience Function
# ============================================================================


textarea = Textarea.create
