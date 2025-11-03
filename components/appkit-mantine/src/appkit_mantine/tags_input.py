"""Mantine TagsInput wrapper for Reflex.

TagsInput component allows entering multiple values as tags.
Built on top of Mantine's Combobox component with tag-based input features.

Docs: https://mantine.dev/core/tags-input/
"""

from __future__ import annotations

from typing import Any

from reflex.event import EventHandler
from reflex.vars.base import Var

from appkit_mantine.base import MantineInputComponentBase


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

    def get_event_triggers(self) -> dict[str, Any]:
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


tags_input = TagsInput.create
