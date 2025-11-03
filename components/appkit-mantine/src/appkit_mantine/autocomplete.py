"""Mantine Autocomplete wrapper for Reflex.

Docs: https://mantine.dev/core/autocomplete/
"""

from __future__ import annotations

from typing import Any

import reflex as rx

from appkit_mantine.base import MantineInputComponentBase


class Autocomplete(MantineInputComponentBase):
    """Reflex wrapper for Mantine Autocomplete.

    Note: Mantine Autocomplete accepts string arrays as `data`. It does not
    support `{value,label}` objects like Select.
    """

    tag = "Autocomplete"

    # Autocomplete-specific props
    data: rx.Var[list[str] | list[dict[str, Any]]]
    limit: rx.Var[int]
    max_dropdown_height: rx.Var[int | str]
    dropdown_opened: rx.Var[bool]
    default_dropdown_opened: rx.Var[bool]
    render_option: rx.Var[Any]
    filter: rx.Var[Any]
    clearable: rx.Var[bool]
    auto_select_on_blur: rx.Var[bool]

    # Event handlers
    on_dropdown_close: rx.EventHandler[rx.event.no_args_event_spec]
    on_dropdown_open: rx.EventHandler[rx.event.no_args_event_spec]
    on_option_submit: rx.EventHandler[lambda value, option: [value, option]]

    _rename_props = {
        **MantineInputComponentBase._rename_props,  # noqa: SLF001
    }

    def get_event_triggers(self) -> dict[str, Any]:
        return {
            **super().get_event_triggers(),
            "on_change": lambda value: [value],
            "on_option_submit": lambda value, option: [value, option],
        }


autocomplete = Autocomplete.create
