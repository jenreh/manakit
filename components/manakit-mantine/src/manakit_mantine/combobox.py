"""Mantine Combobox wrapper for Reflex.

Docs: https://mantine.dev/core/combobox/
"""

from __future__ import annotations

from typing import Any, Literal

import reflex as rx
from reflex.vars.base import Var

from manakit_mantine.base import MantineComponentBase, MantineInputComponentBase


class Combobox(MantineInputComponentBase):
    tag = "Combobox"

    # Arrow
    arrow_offset: rx.Var[int]
    arrow_position: rx.Var[Literal["center", "side"]]
    arrow_radius: rx.Var[int]
    arrow_size: rx.Var[int]

    disabled: rx.Var[bool]

    dropdown_padding: rx.Var[str | int]
    floating_strategy: rx.Var[Literal["absolute", "fixed"]]
    hide_detached: rx.Var[bool]
    keep_mounted: rx.Var[bool]

    # Floating ui middlewares to configure position handling, { flip: true, shift: true, inline: false } by default
    # middlewares: rx.Var[MiddlewaresProps | dict[str, Any]]

    offset: rx.Var[int]
    overlay_props: rx.Var[dict[str, Any]]
    portal_props: rx.Var[dict[str, Any]]
    position: rx.Var[Literal["top", "bottom", "left", "right"]]
    position_dependencies: rx.Var[list[Any]]
    radius: rx.Var[str | int]
    reset_selection_on_option_hover: rx.Var[bool]
    return_focus: rx.Var[bool]
    shadow: rx.Var[str]
    store: rx.Var[Any] = rx.Var.create("combobox")
    transition_props: rx.Var[dict[str, Any]]
    width: rx.Var[str | int | Literal["target"]]
    with_arrow: rx.Var[bool]
    with_overlay: rx.Var[bool]
    with_portal: rx.Var[bool]
    z_index: rx.Var[int]

    on_close: rx.EventHandler[rx.event.no_args_event_spec]
    on_dismiss: rx.EventHandler[rx.event.no_args_event_spec]
    on_enter_transition_end: rx.EventHandler[rx.event.no_args_event_spec]
    on_exit_transition_end: rx.EventHandler[rx.event.no_args_event_spec]
    on_open: rx.EventHandler[rx.event.no_args_event_spec]
    on_option_submit: rx.EventHandler[
        rx.event.passthrough_event_spec(tuple[str, dict[str, Any]])
    ]
    on_position_change: rx.EventHandler[rx.event.passthrough_event_spec(float)]

    def add_hooks(self) -> list[Var]:
        """Add hooks to the component."""
        combobox_hook = rx.Var(
            "const combobox = useCombobox()",
            _var_data=rx.vars.VarData(
                imports={"@mantine/core": "useCombobox"},
                position=rx.constants.Hooks.HookPosition.PRE_TRIGGER,
            ),
        )
        return [combobox_hook]

    def get_event_triggers(self) -> dict[str, Any]:
        def _on_option_submit(value: Var) -> list[Var]:
            return [rx.Var(f"({value} ?? '')", _var_type=str)]

        return {
            **super().get_event_triggers(),
            "onOptionSubmit": _on_option_submit,
        }


class ComboboxOptions(MantineComponentBase):
    """Combobox.Options sub-component."""

    tag = "Combobox.Options"


class ComboboxOption(MantineComponentBase):
    """Combobox.Option sub-component."""

    tag = "Combobox.Option"

    active: rx.Var[bool]
    disabled: rx.Var[bool]
    selected: rx.Var[bool]
    value: rx.Var[str]


class ComboboxTarget(MantineComponentBase):
    """Combobox.Target sub-component."""

    tag = "Combobox.Target"
    _rename_props = {"target": "children"}

    autocomplete: rx.Var[str]
    target: rx.Var[Any]
    ref_prop: rx.Var[str]
    target_type: rx.Var[Literal["button", "input"]]
    with_aria_attributes: rx.Var[bool] = True
    with_expandedattribute: rx.Var[bool] = False
    with_keyboard_navigation: rx.Var[bool] = True


class ComboboxDropdownTarget(MantineComponentBase):
    tag = "Combobox.DropdownTarget"
    _rename_props = {"target": "children"}

    target: rx.Var[Any]
    ref_prop: rx.Var[str]


class ComboboxEventsTarget(MantineComponentBase):
    tag = "Combobox.EventsTarget"


class ComboboxDropdown(MantineComponentBase):
    """Combobox.Dropdown sub-component."""

    tag = "Combobox.Dropdown"

    # Dropdown props
    hidden: Var[bool] = None


class ComboboxGroup(MantineComponentBase):
    tag = "Combobox.Group"

    label: rx.Var[rx.Component | str]


class ComboboxSeparator(MantineComponentBase):
    tag = "Combobox.Separator"


class ComboboxChevron(MantineComponentBase):
    tag = "Combobox.Chevron"


class ComboboxEmpty(MantineComponentBase):
    tag = "Combobox.Empty"


# Convenience functions


class ComboboxNamespace(rx.ComponentNamespace):
    """Namespace for Combobox components."""

    __call__ = staticmethod(Combobox.create)
    chevron = staticmethod(ComboboxChevron.create)
    dropdown = staticmethod(ComboboxDropdown.create)
    dropdown_target = staticmethod(ComboboxDropdownTarget.create)
    empty = staticmethod(ComboboxEmpty.create)
    events_target = staticmethod(ComboboxEventsTarget.create)
    group = staticmethod(ComboboxGroup.create)
    option = staticmethod(ComboboxOption.create)
    options = staticmethod(ComboboxOptions.create)
    separator = staticmethod(ComboboxSeparator.create)
    target = staticmethod(ComboboxTarget.create)


combobox = ComboboxNamespace()
