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
    on_change: EventHandler[lambda value: [value]] = None
    placeholder: Var[str] = "Pick value"
    searchable: Var[bool] = True
    clearable: Var[bool] = False
    nothing_found: Var[str] = "Nothing found"
    max_dropdown_height: Var[int] = 280
    # Kinder: RichSelectItem

    def get_event_triggers(self) -> dict[str, Any]:
        """Ensure event handlers forward Mantine values as list[Var].

        Mantine sends simple values (not events) for on_change/on_option_submit
        so we must return them as a single-item list for Reflex event system.
        """

        def _forward(value: Var) -> list[Var]:
            return [value]

        return {
            **super().get_event_triggers(),
            "on_change": _forward,
            "on_option_submit": _forward,
            "on_search_change": _forward,
        }


class RichSelectItem(rx.Component):
    """Virtuelles Kind - trägt die Daten + Renderer-Node."""

    library = f"$/public{_JSX}"
    tag = "RichSelectItem"

    value: Var[str]
    option: Var[Any]
    disabled: Var[bool] = False
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
        **NEU:** Vergibt einen stabilen React-Key pro Item (rs-<value>), um
        Kollisionen von Default-Keys (z.B. 'row_rx_state_') zu vermeiden.
        """
        if renderer is None and "rendere" in kwargs:
            renderer = kwargs.pop("rendere")
        if renderer is None:
            raise ValueError("rich_select.map(...): 'renderer' ist erforderlich.")

        def _val(row: Any) -> str:
            if value is not None:
                return str(value(row))
            if isinstance(row, dict) and value_key in row:
                return str(row[value_key])
            return str(row)

        def _disabled(row: Any) -> bool:
            if disabled is not None:
                return bool(disabled(row))
            if isinstance(row, dict):
                return bool(row.get("disabled", False))
            return False

        def _keywords(row: Any) -> list[str] | None:
            if keywords is not None:
                return keywords(row)
            if isinstance(row, dict):
                return row.get("keywords")
            return None

        def _payload(row: Any) -> dict[str, Any] | None:
            if payload is not None:
                return payload(row)
            return row if isinstance(row, dict) else {"value": _val(row)}

        def _mapper(row: Any) -> rx.Component:
            v = _val(row)
            return RichSelectItem.create(
                value=v,
                option=renderer(row),
                disabled=_disabled(row),
                keywords=_keywords(row),
                payload=_payload(row),
                key=f"rs-{v}",  # <<< stabiler Key am unmittelbaren Kind
            )

        return rx.foreach(data, _mapper)


# Öffentliche API im Reflex-Stil
rich_select = RichSelectNamespace()
