# components/manakit-mantine/src/manakit_mantine/rich_select.py

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

# Lokales Asset (kein npm "rich_select" mehr!)
_JSX = rx.asset("rich_select.jsx", shared=True)


"""Mantine Combobox (RichSelect) wrapper for Reflex.

This module exposes a comprehensive set of props that map to Mantine's
`Combobox` / `useCombobox` options and Combobox subcomponents. See:
https://mantine.dev/core/combobox/

Notes:
- Python prop names use snake_case and map to Mantine camelCase props.
- `store` is exposed as a passthrough Var[Any] so callers can provide a JS
  combobox store created via Mantine's `useCombobox` hook.
"""


class RichSelect(rx.Component):
    """Reflex wrapper um die JSX-Komponente (Mantine Combobox mapping).

    Mantine prop -> Python mapping examples:
    - defaultOpened -> default_opened
    - onDropdownOpen -> on_dropdown_open
    - classNames -> class_names
    """

    library = f"$/public{_JSX}"
    tag = "RichSelect"

    # Core props (existing)
    value: Var[str | None]
    placeholder: Var[str]
    nothing_found: Var[str] = "Nothing found"

    # Search and clear
    searchable: Var[bool] = True
    clearable: Var[bool] = False
    search_placeholder: Var[str] = "Search..."
    search_value: Var[str] | None = None

    # Dropdown control (useCombobox options)
    default_opened: Var[bool]
    opened: Var[bool]
    loop: Var[bool]
    scroll_behavior: Var[Literal["auto", "instant", "smooth"]]

    # Store passthrough - allows passing Mantine's useCombobox store from JS
    store: Var[Any]

    # Popover/dropdown passthroughs
    position: (
        Var[
            Literal[
                "top",
                "bottom",
                "left",
                "right",
                "top-start",
                "top-end",
                "bottom-start",
                "bottom-end",
                "left-start",
                "left-end",
                "right-start",
                "right-end",
            ]
        ]
        | None
    ) = None
    middlewares: Var[list[Any] | None] = None
    hidden: Var[bool]

    # Dropdown sizing
    max_dropdown_height: Var[int] = 280
    max_height: Var[str | int]
    min_height: Var[str | int]
    height: Var[str | int]

    # Size and appearance
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]
    radius: Var[str | int]
    disabled: Var[bool] = False

    # Styles API / appearance
    class_names: Var[dict[str, str] | None] = None
    styles: Var[dict[str, Any] | None] = None
    unstyled: Var[bool] = False

    # Creatable / new option support
    creatable: Var[bool] = False

    # Multiselect (optional)
    values: Var[list[str] | None] = None

    # Form / accessibility
    aria_label: Var[str] | None = None
    name: Var[str] | None = None
    id: Var[str] | None = None

    # Events
    on_create: EventHandler[lambda value: [value]]
    """Called when a new option is created (receives created value)."""

    on_change: EventHandler[lambda value: [value]]
    """Called when value changes (receives selected value or list of values)."""

    on_search_change: EventHandler[lambda value: [value]]
    """Called when search value changes."""

    on_clear: EventHandler[list]
    """Called when the clear button is clicked."""

    on_option_submit: EventHandler[lambda value: [value]]
    """Called when option is submitted from dropdown."""

    on_opened_change: EventHandler[lambda opened: [opened]]
    """Called when opened state changes."""

    on_dropdown_close: EventHandler[lambda source: [source]]
    """Called when dropdown is closed."""

    on_dropdown_open: EventHandler[lambda source: [source]]
    """Called when dropdown is opened or closed."""
    # Extra props passthrough - JS side expects `extra_props` dict for safe
    # forwarding of nested props (combobox, input_base, search, nothing_found).
    extra_props: Var[dict[str, Any] | None] = None


class RichSelectItem(rx.Component):
    """Virtuelles Kind - trägt die Daten + Renderer-Node."""

    library = f"$/public{_JSX}"
    tag = "RichSelectItem"

    value: Var[str]
    option: Var[Any]
    disabled: Var[bool | None] = False
    keywords: Var[list[str] | None]
    payload: Var[dict[str, Any] | None]
    active: Var[bool] | None = None
    group: Var[str] | None = None


class RichSelectNamespace(rx.ComponentNamespace):
    __call__ = staticmethod(RichSelect.create)
    item = staticmethod(RichSelectItem.create)

    @staticmethod
    def map(
        data: Any,
        renderer: Callable[[Any], rx.Component] | None = None,
        *,
        value: Callable[[Any], str] | None = None,
        value_key: str = "value",
        disabled: Callable[[Any], bool] | None = None,
        keywords: Callable[[Any], list[str] | None] | None = None,
        payload: Callable[[Any], dict[str, Any] | None] | None = None,
        **kwargs,
    ) -> rx.Component:
        """
        Zucker: Daten -> <rich_select.item .../> via rx.foreach.
        **NEU:** Vergibt einen stabilen React-Key pro Item (rs-<index>), um
        Kollisionen von Default-Keys (z.B. 'row_rx_state_') zu vermeiden.
        """
        if renderer is None and "rendere" in kwargs:
            renderer = kwargs.pop("rendere")
        if renderer is None:
            raise ValueError("rich_select.map(...): 'renderer' ist erforderlich.")

        def _mapper(row: Any, index: int) -> rx.Component:
            if value is not None:
                value_var = value(row)
            elif isinstance(row, dict) or (hasattr(row, "__getitem__")):
                value_var = row[value_key]
            else:
                value_var = row

            if disabled is not None:
                disabled_var = disabled(row)
            elif isinstance(row, dict) or (
                hasattr(row, "__getitem__") and hasattr(row, "get")
            ):
                disabled_var = row.get("disabled", False)
            else:
                disabled_var = False

            if keywords is not None:
                keywords_var = keywords(row)
            elif isinstance(row, dict) or (
                hasattr(row, "__getitem__") and hasattr(row, "get")
            ):
                keywords_var = row.get("keywords")
            else:
                keywords_var = None

            if payload is not None:  # noqa: SIM108
                payload_var = payload(row)
            else:
                payload_var = row

            # Create unique key using index
            key_str = f"rs-{index}"

            return RichSelectItem.create(
                value=value_var,
                option=renderer(row),
                disabled=disabled_var,
                keywords=keywords_var,
                payload=payload_var,
                key=key_str,
            )

        return rx.foreach(data, _mapper)


# Öffentliche API im Reflex-Stil
rich_select = RichSelectNamespace()
