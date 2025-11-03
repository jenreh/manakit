from __future__ import annotations

from typing import Any, Literal

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

from appkit_mantine.base import MantineComponentBase


class Button(MantineComponentBase):
    """Mantine Button wrapper for Reflex.

    See: https://mantine.dev/core/button/

    Supports variants, sizes (including compact variants), radius, gradient,
    loading/loaderProps, left/right sections, fullWidth, justify and other
    common Button props.
    """

    tag = "Button"

    _rename_props = {
        "left_section": "leftSection",
        "right_section": "rightSection",
        "loader_props": "loaderProps",
        "aria_label": "aria-label",
        "data_disabled": "data-disabled",
        "full_width": "fullWidth",
        "auto_contrast": "autoContrast",
    }

    # Appearance
    variant: Var[
        Literal[
            "filled",
            "light",
            "subtle",
            "outline",
            "default",
            "gradient",
            "link",
        ]
    ] = None
    color: Var[str] = None
    size: Var[str] = None  # supports xs..xl and compact- variants (use string)
    radius: Var[Literal["xs", "sm", "md", "lg", "xl"]] = None
    gradient: Var[dict] = None

    # Layout
    full_width: Var[bool] = None
    justify: Var[str] = None

    # Sections
    left_section: Var[Any] = None
    right_section: Var[Any] = None

    # Compact sizes support via naming (e.g., "compact-md") — accept string

    # State
    disabled: Var[bool] = None
    data_disabled: Var[bool] = None
    loading: Var[bool] = None

    # Loader customization
    loader_props: Var[dict] = None

    # Accessibility & HTML
    aria_label: Var[str] = None
    component: Var[str] = None
    type: Var[Literal["button", "submit", "reset"]] = None

    # Misc
    auto_contrast: Var[bool] = None

    # Content
    children: Var[Any] = None

    # Events
    on_click: EventHandler[rx.event.no_args_event_spec] = None


class ButtonNamespace(rx.ComponentNamespace):
    """Namespace factory for Button to match other component patterns."""

    __call__ = staticmethod(Button.create)


button = ButtonNamespace()
