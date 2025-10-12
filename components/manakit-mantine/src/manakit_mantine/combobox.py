"""Mantine Combobox wrapper for Reflex.

This component provides a flexible combobox implementation that replaces
Mantine's useCombobox hook with a Reflex-compatible store system.

Docs: https://mantine.dev/core/combobox/
"""

from __future__ import annotations

from typing import Any, Literal

import reflex as rx
from reflex.constants import Hooks
from reflex.event import EventHandler
from reflex.vars import VarData
from reflex.vars.base import Var

from manakit_mantine.base import MantineComponentBase


class ComboboxComponentBase(MantineComponentBase):
    """Base class for all Combobox-related components."""


class Combobox(ComboboxComponentBase):
    """Mantine Combobox main component."""

    tag = "Combobox"

    # Store - will be set to reference the useCombobox hook
    store: Var[Any] = rx.Var.create("combobox")

    # Dropdown positioning
    position: Var[Literal["top", "bottom", "left", "right"]]
    offset: Var[int]
    width: Var[str | int | Literal["target"]]  # noqa: PYI051

    # Visual styling
    shadow: Var[str]
    radius: Var[str | int]
    dropdown_padding: Var[str | int]
    with_arrow: Var[bool]
    arrow_size: Var[int]
    arrow_offset: Var[int]
    arrow_position: Var[Literal["center", "side"]]
    arrow_radius: Var[int]

    # Behavior
    disabled: Var[bool]
    keep_mounted: Var[bool]
    with_portal: Var[bool]
    z_index: Var[int]
    return_focus: Var[bool]
    reset_selection_on_option_hover: Var[bool]

    # Advanced positioning
    floating_strategy: Var[Literal["absolute", "fixed"]]
    hide_detached: Var[bool]
    position_dependencies: Var[list[Any]]

    # Transitions
    transition_props: Var[dict[str, Any]]

    # Events
    on_option_submit: EventHandler[lambda value, details: [value, details]]
    on_open: EventHandler[list]
    on_close: EventHandler[list]
    on_dismiss: EventHandler[list]

    def add_hooks(self) -> list[Var]:
        """Inject the `useCombobox` hook into the compiled component scope.

        This creates a `combobox` variable in component scope using a Var so
        Mantine internals (which expect a combobox store on `ctx.store`) can
        call methods like `setListId` on it.
        """
        combobox_hook = rx.Var(
            "const combobox = useCombobox()",
            _var_data=VarData(
                # imports={"@mantine/core": "useCombobox"},
                position=Hooks.HookPosition.PRE_TRIGGER,
            ),
        )
        return [combobox_hook]


class ComboboxTarget(ComboboxComponentBase):
    """Target element wrapper - wraps the element that opens dropdown."""

    tag = "Combobox.Target"

    _rename_props = {"target": "children"}

    target: Var[Any]  # The target element (mapped to children)
    ref_prop: Var[str]
    target_type: Var[Literal["button", "input"]]
    with_aria_attributes: Var[bool]
    with_expanded_attribute: Var[bool]
    with_keyboard_navigation: Var[bool]


class ComboboxDropdown(ComboboxComponentBase):
    """Dropdown element wrapper - contains the options list."""

    tag = "Combobox.Dropdown"

    hidden: Var[bool]


class ComboboxOptions(ComboboxComponentBase):
    """Options list wrapper - wraps multiple Option components."""

    tag = "Combobox.Options"


class ComboboxOption(ComboboxComponentBase):
    """Individual option in the combobox."""

    tag = "Combobox.Option"

    value: Var[str]
    active: Var[bool]
    disabled: Var[bool]
    selected: Var[bool]


class ComboboxGroup(ComboboxComponentBase):
    """Group of related options with optional label."""

    tag = "Combobox.Group"

    label: Var[str]


class ComboboxSearch(ComboboxComponentBase):
    """Search input for filtering options."""

    tag = "Combobox.Search"

    placeholder: Var[str]
    value: Var[str]
    on_change: EventHandler[lambda value: [value]]
    on_input: EventHandler[lambda value: [value]]


class ComboboxEmpty(ComboboxComponentBase):
    """Empty state component when no options match."""

    tag = "Combobox.Empty"


class ComboboxChevron(ComboboxComponentBase):
    """Chevron icon component for dropdown indicator."""

    tag = "Combobox.Chevron"

    size: Var[str | int]
    error: Var[bool]


class ComboboxDropdownTarget(ComboboxComponentBase):
    """Alternative dropdown target wrapper."""

    tag = "Combobox.DropdownTarget"

    _rename_props = {"target": "children"}

    target: Var[Any]
    ref_prop: Var[str]


class ComboboxEventsTarget(ComboboxTarget):
    """Events target element wrapper."""

    tag = "Combobox.EventsTarget"


class ComboboxFooter(ComboboxComponentBase):
    """Footer section in dropdown."""

    tag = "Combobox.Footer"


class ComboboxHeader(ComboboxComponentBase):
    """Header section in dropdown."""

    tag = "Combobox.Header"


# Namespace for clean API
class ComboboxNamespace(rx.ComponentNamespace):
    """Namespace for Combobox components."""

    __call__ = staticmethod(Combobox.create)
    chevron = staticmethod(ComboboxChevron.create)
    dropdown = staticmethod(ComboboxDropdown.create)
    dropdown_target = staticmethod(ComboboxDropdownTarget.create)
    empty = staticmethod(ComboboxEmpty.create)
    events_target = staticmethod(ComboboxEventsTarget.create)
    footer = staticmethod(ComboboxFooter.create)
    group = staticmethod(ComboboxGroup.create)
    header = staticmethod(ComboboxHeader.create)
    option = staticmethod(ComboboxOption.create)
    options = staticmethod(ComboboxOptions.create)
    search = staticmethod(ComboboxSearch.create)
    target = staticmethod(ComboboxTarget.create)


# Export the namespace
combobox = ComboboxNamespace()
