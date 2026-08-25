"""Mantine miscellaneous inputs: TagsInput, NativeSelect, FileInput, Fieldset,
Chip, and Chip.Group."""

from __future__ import annotations

from typing import Any, Literal

from reflex.event import EventHandler
from reflex.vars.base import Var

from appkit_mantine.base import MantineInputComponentBase, MantineLayoutComponentBase


class TagsInput(MantineInputComponentBase):
    """Reflex wrapper for Mantine TagsInput.

    TagsInput provides a way to enter multiple values as tags. Users can type
    values and press Enter to create tags, or select from predefined options.
    Supports various data formats and features like max tags limit, duplicates
    control, and split characters.

    Inherits common input props from MantineInputComponentBase. Use `data` as
    list[str], list[dict(value,label)], or grouped format.

    Example:
        ```python
        mn.tags_input(
            label="Skills",
            data=["React", "Python", "JavaScript", "TypeScript"],
            value=state.skills,
            on_change=state.set_skills,
            max_tags=5,
        )
        ```
    """

    tag = "TagsInput"

    # Core data and value props
    data: Var[list[Any]] = None
    """Data used to generate options. Values must be unique."""

    # Tag creation behavior
    # Defaults match Mantine TagsInput (see mantine source)
    accept_value_on_blur: Var[bool] = True
    """If set, the value is accepted when the input loses focus. Defaults to True."""

    allow_duplicates: Var[bool] = False
    """If set, duplicate tags are allowed. Defaults to False."""

    max_tags: Var[int] = None
    """Maximum number of tags that can be added.
    Mantine default is Infinity when omitted.
    """

    split_chars: Var[list[str]] = [","]
    """Characters that should be used to split input value into tags.
    Defaults to [','].
    """

    # Search and filtering - Mantine supports controlled searchValue and onSearchChange
    search_value: Var[str] = None
    """Controlled search value."""

    default_search_value: Var[str] = None
    """Default search value."""

    filter: Var[Any] = None
    """Function based on which items are filtered and sorted."""

    # Visual options
    render_option: Var[Any] = None
    """Function to render option in dropdown."""

    render_pill: Var[Any] = None
    """Function to render pill (Mantine 9+)."""

    # Clear functionality
    clearable: Var[bool] = False
    """If set, the clear button is displayed in the right section. Defaults to False."""

    # Dropdown behavior
    limit: Var[int] = None
    """Maximum number of options displayed at a time."""

    # Align with Mantine's common dropdown default (OptionsDropdown uses 220px mah)
    max_dropdown_height: Var[str | int] = 220

    with_scroll_area: Var[bool] = True
    """Determines whether the options should be wrapped with ScrollArea.
    Defaults to True.
    """

    floating_height: Var[str | int] = None
    """Dropdown height mode (Mantine 9.3). ``"viewport"`` fills vertical space."""

    # Combobox integration
    combobox_props: Var[dict[str, Any]] = None
    """Props passed down to the underlying Combobox component."""

    # Event handlers
    on_search_change: EventHandler[lambda value: [value]] = None
    """Called when search value changes."""

    on_duplicate: EventHandler[lambda value: [value]] = None
    """Called when user attempts to add a duplicate tag."""

    on_remove: EventHandler[lambda value: [value]] = None
    """Called when a tag is removed (alias for Mantine onRemove)."""

    on_clear: EventHandler[list] = None
    """Called when the clear button is clicked."""

    on_dropdown_close: EventHandler[list] = None
    """Called when dropdown closes."""

    on_dropdown_open: EventHandler[list] = None
    """Called when dropdown opens."""

    on_option_submit: EventHandler[lambda value: [value]] = None
    """Called when option is submitted from dropdown."""

    # (on_remove is the Mantine prop name; keep that as primary)

    @classmethod
    def get_event_triggers(cls) -> dict[str, Any]:
        """Transform events to work with Reflex state system.

        TagsInput sends array values directly from Mantine, so we forward them
        as-is to maintain the array structure expected by Reflex state.
        """

        def _on_change(value: Var) -> list[Var]:
            # Mantine TagsInput sends the array directly, forward it as-is
            return [value]

        return {
            **super().get_event_triggers(),
            "on_change": _on_change,
        }


class NativeSelect(MantineInputComponentBase):
    """Mantine NativeSelect component — native browser select element.

    https://mantine.dev/core/native-select/
    """

    tag = "NativeSelect"

    data: Var[list[Any]] = None
    """Options as list of strings or {value, label, disabled?} dicts."""


class FileInput(MantineInputComponentBase):
    """Mantine FileInput component — file picker with input wrapper.

    https://mantine.dev/core/file-input/
    """

    tag = "FileInput"

    _rename_props = {
        **MantineInputComponentBase._rename_props,  # noqa: SLF001
        "accept": "accept",
        "capture": "capture",
        "clearable": "clearable",
        "multiple": "multiple",
        "value_component": "valueComponent",
    }

    accept: Var[str] = None
    capture: Var[str | bool] = None
    multiple: Var[bool] = None
    clearable: Var[bool] = None
    value_component: Var[Any] = None

    @classmethod
    def get_event_triggers(cls) -> dict[str, Any]:
        def _on_change(value: Var) -> list[Var]:
            return [value]

        return {
            **super().get_event_triggers(),
            "on_change": _on_change,
        }


class Fieldset(MantineLayoutComponentBase):
    """Mantine Fieldset component — groups related inputs with a legend.

    https://mantine.dev/core/fieldset/
    """

    tag = "Fieldset"

    legend: Var[Any] = None
    radius: Var[str | int] = None
    disabled: Var[bool] = None
    variant: Var[Literal["default", "filled", "unstyled"]] = None


class Chip(MantineLayoutComponentBase):
    """Mantine Chip component — toggleable chip/tag input.

    https://mantine.dev/core/chip/
    """

    tag = "Chip"

    _rename_props = {
        "auto_contrast": "autoContrast",
        "default_checked": "defaultChecked",
    }

    auto_contrast: Var[bool] = None
    checked: Var[bool] = None
    color: Var[str] = None
    default_checked: Var[bool] = None
    disabled: Var[bool] = None
    icon: Var[Any] = None
    id: Var[str] = None
    radius: Var[str | int] = None
    size: Var[str | int] = None
    type: Var[Literal["checkbox", "radio"]] = None
    value: Var[str] = None
    variant: Var[Literal["outline", "light", "filled"]] = None

    on_change: EventHandler[lambda checked: [checked]] = None


class ChipGroup(MantineLayoutComponentBase):
    """Mantine Chip.Group component — manages multiple Chip selections.

    https://mantine.dev/core/chip/
    """

    tag = "Chip.Group"

    _rename_props = {
        "default_value": "defaultValue",
    }

    value: Var[str | list[str]] = None
    default_value: Var[str | list[str]] = None
    multiple: Var[bool] = None

    on_change: EventHandler[lambda value: [value]] = None
