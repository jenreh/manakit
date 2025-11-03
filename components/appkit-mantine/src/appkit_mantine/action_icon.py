from __future__ import annotations

from typing import Any, Literal

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

from appkit_mantine.base import MantineComponentBase


class ActionIcon(MantineComponentBase):
    """Mantine ActionIcon component wrapper for Reflex.

    See: https://mantine.dev/core/action-icon/

    This component is a lightweight button intended to hold an icon.
    It supports size, variant, radius and disabled state. Use the
    `action_icon` factory at the bottom for convenience.
    """

    tag = "ActionIcon"

    # Prop aliasing for camelCase/HTML attributes
    _rename_props = {
        "aria_label": "aria-label",
        "data_disabled": "data-disabled",
        "loader_props": "loaderProps",
        "auto_contrast": "autoContrast",
    }

    # Appearance
    # size accepts any CSS value (number treated as px) — use str|int for flexibility
    size: Var[str | int] = None
    variant: Var[
        Literal[
            "filled",
            "light",
            "subtle",
            "outline",
            "default",
            "transparent",
            "gradient",
        ]
    ] = None
    radius: Var[Literal["xs", "sm", "md", "lg", "xl"]] = None

    # State
    disabled: Var[bool] = None
    data_disabled: Var[bool] = None
    loading: Var[bool] = None

    # Color and styles
    color: Var[str] = None
    auto_contrast: Var[bool] = None
    gradient: Var[dict] = None

    # Icon/content
    children: Var[Any] = None

    # HTML/button attributes
    # Polymorphic component prop - can change the underlying element
    component: Var[str] = None

    type: Var[Literal["button", "submit", "reset"]] = None
    aria_label: Var[str] = None

    # Event handlers
    on_click: EventHandler[rx.event.no_args_event_spec] = None
    # Loader customization
    loader_props: Var[dict] = None


class ActionIconGroup(MantineComponentBase):
    """Mantine ActionIcon.Group wrapper.

    Used to group multiple ActionIcon components with consistent spacing
    and orientation. Children should be only `ActionIcon` or `ActionIcon.GroupSection`.
    """

    tag = "ActionIcon.Group"

    # Layout and visual group props
    orientation: Var[Literal["horizontal", "vertical"]] = None
    spacing: Var[str | int] = None
    gap: Var[str | int] = None
    no_wrap: Var[bool] = None
    unstyled: Var[bool] = None
    # Optional visual separator between group items. If provided, it will be
    # rendered between children. Accepts any component (string or rx.Component)
    separator: Var[Any] = None
    separator_props: Var[dict] = None
    children: Var[Any] = None


class ActionIconGroupSection(MantineComponentBase):
    """Mantine ActionIcon.GroupSection wrapper.

    Use to render non-ActionIcon elements inside an ActionIcon.Group (for example
    separators or labels). Keeps layout consistent with the group.
    """

    tag = "ActionIcon.GroupSection"

    # Content
    children: Var[Any] = None


class ActionIconNamespace(rx.ComponentNamespace):
    """Namespace factory for ActionIcon to match other components."""

    __call__ = staticmethod(ActionIcon.create)
    group = staticmethod(ActionIconGroup.create)
    group_section = staticmethod(ActionIconGroupSection.create)


action_icon = ActionIconNamespace()
