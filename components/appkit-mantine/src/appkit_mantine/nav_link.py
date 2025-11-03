from __future__ import annotations

from typing import Any, Literal

from reflex.event import EventHandler
from reflex.vars.base import Var

from appkit_mantine.base import MantineComponentBase


class NavLink(MantineComponentBase):
    """Mantine NavLink wrapper for Reflex.

    See: https://mantine.dev/core/nav-link/

    Supports label, description, icon, right_section, children (nested links),
    opened/default_opened control, active/disabled states, styles and sx.
    """

    tag = "NavLink"

    # Prop renames from snake_case to camelCase / React names
    _rename_props = {
        "aria_label": "aria-label",
        "right_section": "rightSection",
        "default_opened": "defaultOpened",
        "initially_opened": "initiallyOpened",
        "chevron_position": "chevronPosition",
    }

    # Basic content
    label: Var[str] = None
    description: Var[str] = None
    icon: Var[Any] = None
    left_section: Var[Any] = None
    right_section: Var[Any] = None
    children: Var[Any] = None

    # Open/active state control
    opened: Var[bool] = None
    default_opened: Var[bool] = None
    initially_opened: Var[bool] = None
    active: Var[bool] = None

    # Visual props
    variant: Var[Literal["default", "filled", "subtle", "outline"]] = None
    color: Var[str] = None
    radius: Var[str] = None
    disabled: Var[bool] = None

    # Chevron position (left/right)
    chevron_position: Var[Literal["left", "right"]] = None

    # Transitions
    transition_duration: Var[int] = None

    # Event handlers
    on_click: EventHandler = None

    # Styling hooks
    styles: Var[dict] = None
    sx: Var[dict] = None


# Convenience factory to match other components' usage
nav_link = NavLink.create
