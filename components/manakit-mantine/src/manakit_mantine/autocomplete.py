"""Mantine Autocomplete wrapper for Reflex.

Docs: https://mantine.dev/core/autocomplete/
"""

from __future__ import annotations

from typing import Any, Literal

import reflex as rx

from .base import MantineInputComponentBase
from .combobox import Combobox


class Autocomplete(Combobox):
    """Reflex wrapper for Mantine Autocomplete.

    Note: Mantine Autocomplete accepts string arrays as `data`. It does not
    support `{value,label}` objects like Select.
    """

    tag = "Autocomplete"

    auto_select_on_blur: rx.Var[bool]
    clear_button_props: rx.Var[dict]
    clearable: rx.Var[bool]
    combobox_props: rx.Var[dict]
    data: rx.Var[list[str] | list[dict[str, Any]]]
    default_dropdown_opened: rx.Var[bool]
    default_value: rx.Var[list[str]]
    disabled: rx.Var[bool]
    dropdown_opened: rx.Var[bool]
    size: rx.Var[Literal["xs", "sm", "md", "lg", "xl"]]
    value: rx.Var[str]
    render_option: rx.Var[Any]
    max_dropdown_height: rx.Var[int | str]

    on_dropdown_close: rx.EventHandler[rx.event.no_args_event_spec]
    on_dropdown_open: rx.EventHandler[rx.event.no_args_event_spec]
    on_option_submit: rx.EventHandler[lambda item: [item]]

    _rename_props = {
        **MantineInputComponentBase._rename_props,  # noqa: SLF001
    }

    def get_event_triggers(self) -> dict[str, Any]:
        def _on_change(value: rx.Var) -> list[rx.Var]:
            return [rx.Var(f"({value} ?? '')", _var_type=str)]

        return {
            **super().get_event_triggers(),
            "on_change": _on_change,
        }


autocomplete = Autocomplete.create
