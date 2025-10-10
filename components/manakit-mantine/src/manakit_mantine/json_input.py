from __future__ import annotations

from collections.abc import Callable
from typing import Any

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

from manakit_mantine.base import MantineInputComponentBase


class JsonInput(MantineInputComponentBase):
    """Mantine JsonInput component wrapper for Reflex.

    Based on https://mantine.dev/core/json-input/

    Inherits all common input props from MantineInputComponentBase and adds
    JSON-specific features like formatting on blur, validation error, parser
    and custom pretty printing.
    """

    tag = "JsonInput"
    alias = "MantineJsonInput"

    # JSON-specific props
    format_on_blur: Var[bool] = None
    """If true, formats (pretty prints) the JSON on blur."""

    # Validation and parsing
    validation_error: Var[str] = None
    """Custom validation error message shown when JSON is invalid."""

    parser: Var[Callable[[str], Any]] = None
    """Optional parser function to parse the input string into JSON value."""

    pretty: Var[bool] = None
    """When formatting, pretty-print the JSON (multi-line) if True."""

    # Textarea-like props (rows/autosize)
    autosize: Var[bool] = None
    min_rows: Var[int] = None
    max_rows: Var[int] = None

    # Events - JsonInput exposes on_change similar to other inputs
    on_change: EventHandler[rx.event.input_event] = None


json_input = JsonInput.create
