from __future__ import annotations

from typing import Literal

from reflex.vars.base import Var

from appkit_mantine.base import MantineInputComponentBase


class NumberFormatter(MantineInputComponentBase):
    """Mantine NumberFormatter wrapper for Reflex.

    See: https://mantine.dev/core/number-formatter/

    This component formats numeric input according to provided parser/formatter
    and exposes on_change receiving the parsed value.
    """

    tag = "NumberFormatter"
    alias = "MantineNumberFormatter"

    # Formatting/parser behavior
    allow_negative: Var[bool] = True
    decimal_scale: Var[int] = None
    decimal_separator: Var[str] = "."
    fixed_decimal_scale: Var[bool] = False
    prefix: Var[str] = None
    suffix: Var[str] = None
    thousand_separator: Var[str | bool] = ","
    thousands_group_style: Var[Literal["thousand", "lakh", "wan", "none"]] = "none"


number_formatter = NumberFormatter.create
