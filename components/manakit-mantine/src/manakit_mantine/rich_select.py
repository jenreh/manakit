# components/manakit-mantine/src/manakit_mantine/rich_select.py
from __future__ import annotations

from collections.abc import Callable
from typing import Any

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

# Lokales Asset (kein npm "rich_select" mehr!)
_JSX = rx.asset("rich_select.jsx", shared=True)


class RichSelect(rx.Component):
    """Reflex wrapper um die JSX-Komponente."""

    library = f"$/public{_JSX}"
    tag = "RichSelect"

    # Props wie gehabt:
    value: Var[str | None]
    placeholder: Var[str] = "Pick value"
    nothing_found: Var[str] = "Nothing found"

    searchable: Var[bool] = True
    clearable: Var[bool] = False

    max_dropdown_height: Var[int] = 280

    on_change: EventHandler[lambda value: [value]]
    """Called when value changes (receives array of selected values)."""

    on_search_change: EventHandler[lambda value: [value]]
    """Called when search value changes."""

    on_clear: EventHandler[list]
    """Called when the clear button is clicked."""

    on_dropdown_close: EventHandler[list]
    """Called when dropdown closes."""

    on_dropdown_open: EventHandler[list]
    """Called when dropdown opens."""

    on_option_submit: EventHandler[lambda value: [value]]
    """Called when option is submitted from dropdown."""


class RichSelectItem(rx.Component):
    """Virtuelles Kind - trägt die Daten + Renderer-Node."""

    library = f"$/public{_JSX}"
    tag = "RichSelectItem"

    value: Var[str]
    option: Var[Any]
    disabled: Var[bool | None] = False
    keywords: Var[list[str] | None]
    payload: Var[dict[str, Any] | None]


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
        **NEU:** Vergibt einen stabilen React-Key pro Item (rs-<value>-<index>), um
        Kollisionen von Default-Keys (z.B. 'row_rx_state_') zu vermeiden.
        """
        if renderer is None and "rendere" in kwargs:
            renderer = kwargs.pop("rendere")
        if renderer is None:
            raise ValueError("rich_select.map(...): 'renderer' ist erforderlich.")

        def _mapper(row: Any, index: int) -> rx.Component:
            # Extract the value Var - don't convert to string!
            if value is not None:
                # Custom value extractor - returns a Var
                value_var = value(row)
            elif isinstance(row, dict) or (hasattr(row, "__getitem__")):
                # Access dict/Var dict-style
                value_var = row[value_key]
            else:
                # Fallback to row itself
                value_var = row

            # Extract disabled Var
            if disabled is not None:
                disabled_var = disabled(row)
            elif isinstance(row, dict) or (
                hasattr(row, "__getitem__") and hasattr(row, "get")
            ):
                disabled_var = row.get("disabled", False)
            else:
                disabled_var = False

            # Extract keywords Var
            if keywords is not None:
                keywords_var = keywords(row)
            elif isinstance(row, dict) or (
                hasattr(row, "__getitem__") and hasattr(row, "get")
            ):
                keywords_var = row.get("keywords")
            else:
                keywords_var = None

            # Extract payload Var
            if payload is not None:  # noqa: SIM108
                payload_var = payload(row)
            else:
                # Default payload is the row itself if it's a dict-like object
                payload_var = row

            # Create unique key by combining value with index
            # Use rx.cond to handle None values gracefully
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
