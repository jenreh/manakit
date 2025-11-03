"""Mantine MultiSelect wrapper for Reflex.

MultiSelect component allows selecting multiple values from a list of options.
Built on top of Mantine's Combobox component with opinionated multi-select features.

Docs: https://mantine.dev/core/multi-select/
"""

from __future__ import annotations

from typing import Any, Literal

from reflex.event import EventHandler, input_event
from reflex.vars.base import Var

from appkit_mantine.base import MantineInputComponentBase


class MultiSelect(MantineInputComponentBase):
    """Reflex wrapper for Mantine MultiSelect.

    MultiSelect provides a way to enter multiple values from predefined options.
    It supports various data formats (strings, objects, groups) and features like
    search, max values limit, and hiding picked options.

    Inherits common input props from MantineInputComponentBase. Use `data` as
    list[str], list[dict(value,label)], or grouped format.

    Example:
        ```python
        mn.multi_select(
            label="Favorite frameworks",
            data=["React", "Vue", "Angular", "Svelte"],
            value=state.selected_frameworks,
            on_change=state.set_selected_frameworks,
            searchable=True,
        )
        ```
    """

    tag = "MultiSelect"

    # Core data and value props
    data: Var[list[Any]] = None
    """Data used to generate options. Values must be unique."""

    # Search and filtering
    searchable: Var[bool] = False
    """Allows searching/filtering options by user input."""

    search_value: Var[str] = None
    """Controlled search value."""

    default_search_value: Var[str] = None
    """Default search value."""

    clear_search_on_change: Var[bool] = False
    """Clear search value when item is selected."""

    filter: Var[Any] = None
    """Function based on which items are filtered and sorted."""

    # Selection behavior
    max_values: Var[int] = None
    """Maximum number of values that can be selected."""

    hide_picked_options: Var[bool] = False
    """If set, picked options are removed from the options list."""

    # Visual options
    check_icon_position: Var[Literal["left", "right"]] = "left"
    """Position of the check icon relative to the option label."""

    with_check_icon: Var[bool] = True
    """If set, check icon is displayed near the selected option label."""

    # Clear functionality
    clearable: Var[bool] = False
    """If set, the clear button is displayed in the right section."""

    # Messages
    nothing_found_message: Var[str] = "No options"
    """Message displayed when no option matches the current search query."""

    # Dropdown behavior
    limit: Var[int] = None
    """Maximum number of options displayed at a time."""

    max_dropdown_height: Var[str | int] = "200px"
    """Max height of the dropdown."""

    with_scroll_area: Var[bool] = True
    """Determines whether the options should be wrapped with ScrollArea."""

    # Combobox integration
    combobox_props: Var[dict[str, Any]] = None
    """Props passed down to the underlying Combobox component."""

    # Event handlers
    on_search_change: EventHandler[input_event] = None
    """Called when search value changes."""

    on_clear: EventHandler[list] = None
    """Called when the clear button is clicked."""

    on_dropdown_close: EventHandler[list] = None
    """Called when dropdown closes."""

    on_dropdown_open: EventHandler[list] = None
    """Called when dropdown opens."""

    on_option_submit: EventHandler[input_event] = None
    """Called when option is submitted from dropdown."""

    def get_event_triggers(self) -> dict[str, Any]:
        """Transform events to work with Reflex state system.

        MultiSelect sends array values directly from Mantine, so we forward them
        as-is to maintain the array structure expected by Reflex state.
        """

        def _on_change(value: Var) -> list[Var]:
            # Mantine MultiSelect sends the array directly, forward it as-is
            return [value]

        return {
            **super().get_event_triggers(),
            "on_change": _on_change,
        }


multi_select = MultiSelect.create
