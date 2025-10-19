# custom_components/rich_select/rich_select.py
from __future__ import annotations

from collections.abc import Callable
from typing import Any

import reflex as rx

_JSX = rx.asset("rich_select.jsx", shared=True)


class RichSelect(rx.Component):
    """Reflex wrapper for the Mantine-based RichSelect component.
    A single renderer (option) is used for the dropdown list and the selected value."""

    # Use our bundled frontend wrapper under assets/public
    library = f"$/public{_JSX}"
    tag = "RichSelect"

    value: str | None
    placeholder: str | None
    searchable: bool = True
    clearable: bool = False
    max_dropdown_height: int | None

    on_change: rx.EventHandler[lambda value: [value]] = None
    on_clear: rx.EventHandler[lambda item: [item]] = None
    on_dropdown_close: rx.EventHandler[lambda item: [item]] = None
    on_dropdown_open: rx.EventHandler[lambda item: [item]] = None
    on_option_submit: rx.EventHandler[lambda item: [item]] = None
    on_search_change: rx.EventHandler[lambda value: [value]] = None


class RichSelectItem(rx.Component):
    """Marker component for a single option (and selected renderer)."""

    library = f"$/public{_JSX}"
    tag = "RichSelectItem"

    value: str
    option: rx.Component
    disabled: bool | None = None
    keywords: list[str] | None = None
    payload: dict[str, Any] | None = None


class RichSelectNamespace(rx.ComponentNamespace):
    __call__ = staticmethod(RichSelect.create)
    item = staticmethod(RichSelectItem.create)

    @staticmethod
    def map(
        data: Any,
        renderer: Callable[[dict[str, Any]], rx.Component] | None = None,
        *,
        value: Callable[[dict[str, Any]], str] | None = None,
        value_key: str = "value",
        disabled: Callable[[dict[str, Any]], Any] | None = None,
        keywords: Callable[[dict[str, Any]], list[str] | None] | None = None,
        payload: Callable[[dict[str, Any]], dict[str, Any] | None] | None = None,
        **kwargs,
    ) -> rx.Component:
        """Sugar function: map data -> <RichSelectItem> list via rx.foreach.

        Args:
            data: Sequence or state var accepted by rx.foreach.
            renderer(row): required. Returns the SINGLE renderer node
                (used in dropdown & selected value).
            value(row): optional. Defaults to row[value_key] or str(row).
            value_key: fallback key ('value').
            disabled(row): optional. Defaults to row.get('disabled', False).
            keywords(row): optional. Defaults to row.get('keywords').
            payload(row): optional. Defaults to the entire row.
        """
        # allow typo alias 'rendere'
        if renderer is None and "rendere" in kwargs:
            renderer = kwargs.pop("rendere")
        if renderer is None:
            raise ValueError("rich_select.map(...): 'renderer' is required.")

        def _val(row: dict[str, Any]) -> str:
            if value is not None:
                return value(row)
            if isinstance(row, dict) and value_key in row:
                return row[value_key]
            return str(row)

        def _disabled(row: dict[str, Any]):
            if disabled is not None:
                return disabled(row)
            if isinstance(row, dict):
                return row.get("disabled", False)
            return False

        def _keywords(row: dict[str, Any]):
            if keywords is not None:
                return keywords(row)
            if isinstance(row, dict):
                return row.get("keywords")
            return None

        def _payload(row: dict[str, Any]):
            if payload is not None:
                return payload(row)
            return row if isinstance(row, dict) else {"value": _val(row)}

        def _mapper(row: dict[str, Any]) -> rx.Component:
            return RichSelectItem.create(
                value=_val(row),
                option=renderer(row),
                disabled=_disabled(row),
                keywords=_keywords(row),
                payload=_payload(row),
            )

        return rx.foreach(data, _mapper)


# Public API instance
rich_select = RichSelectNamespace()
