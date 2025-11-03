"""Mantine PasswordInput component wrapper for Reflex.

Provides a password input with visibility toggle functionality.
See `mantine_password_input()` function for detailed usage and examples.
"""

from __future__ import annotations

from typing import Any

from reflex.event import EventHandler
from reflex.vars.base import Var

from appkit_mantine.base import (
    MantineInputComponentBase,
)


class PasswordInput(MantineInputComponentBase):
    """Mantine PasswordInput component with visibility toggle.

    Based on: https://mantine.dev/core/password-input/

    Inherits common input props from MantineInputComponentBase.
    See `mantine_password_input()` function for detailed documentation and examples.
    """

    tag = "PasswordInput"

    # Password visibility control
    visible: Var[bool] = None
    """Control password visibility state (controlled component)."""

    default_visible: Var[bool] = None
    """Default visibility state (uncontrolled component)."""

    # Visibility toggle customization
    visibility_toggle_icon: Var[Any] = None
    """Custom icon component for the visibility toggle button."""

    visibility_toggle_button_props: Var[dict] = None
    """Props to pass to the visibility toggle button."""

    # Event handlers (password-specific)
    on_visibility_change: EventHandler[lambda visible: [visible]] = None
    """Called when visibility toggle is clicked (receives boolean)."""


# ============================================================================
# Convenience Function
# ============================================================================


password_input = PasswordInput.create
