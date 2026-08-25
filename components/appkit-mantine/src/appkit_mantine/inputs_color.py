"""Mantine color inputs: ColorInput, ColorPicker, AlphaSlider, and HueSlider."""

from __future__ import annotations

from typing import Any, Literal

import reflex as rx
from reflex.event import EventHandler
from reflex.vars.base import Var

from appkit_mantine.base import MantineInputComponentBase, MantineLayoutComponentBase


class ColorInput(MantineInputComponentBase):
    """Mantine ColorInput component — color picker combined with text input.

    https://mantine.dev/core/color-input/
    """

    tag = "ColorInput"

    _rename_props = {
        **MantineInputComponentBase._rename_props,  # noqa: SLF001
        "close_on_color_swatch_click": "closeOnColorSwatchClick",
        "disallow_input": "disallowInput",
        "eye_dropper_button_props": "eyeDropperButtonProps",
        "eye_dropper_icon": "eyeDropperIcon",
        "fix_on_blur": "fixOnBlur",
        "full_width": "fullWidth",
        "on_change_end": "onChangeEnd",
        "popover_props": "popoverProps",
        "swatches_per_row": "swatchesPerRow",
        "with_eye_dropper": "withEyeDropper",
        "with_picker": "withPicker",
        "with_preview": "withPreview",
    }

    format: Var[Literal["hex", "hexa", "rgba", "rgb", "hsl", "hsla"]] = None
    swatches: Var[list[str]] = None
    swatches_per_row: Var[int] = None
    with_picker: Var[bool] = None
    with_preview: Var[bool] = None
    with_eye_dropper: Var[bool] = None
    disallow_input: Var[bool] = None
    close_on_color_swatch_click: Var[bool] = None
    fix_on_blur: Var[bool] = None
    full_width: Var[bool] = None
    popover_props: Var[dict] = None
    eye_dropper_icon: Var[Any] = None

    on_change_end: EventHandler[lambda value: [value]] = None

    @classmethod
    def get_event_triggers(cls) -> dict[str, Any]:
        def _on_change(value: Var) -> list[Var]:
            return [value]

        return {
            **super().get_event_triggers(),
            "on_change": _on_change,
        }


class ColorPicker(MantineLayoutComponentBase):
    """Mantine ColorPicker component — standalone color picker UI.

    https://mantine.dev/core/color-picker/
    """

    tag = "ColorPicker"

    _rename_props = {
        "alpha_label": "alphaLabel",
        "default_value": "defaultValue",
        "full_width": "fullWidth",
        "hidden_input_props": "hiddenInputProps",
        "hue_label": "hueLabel",
        "on_change_end": "onChangeEnd",
        "on_color_swatch_click": "onColorSwatchClick",
        "saturation_label": "saturationLabel",
        "swatches_per_row": "swatchesPerRow",
        "with_picker": "withPicker",
    }

    value: Var[str] = None
    default_value: Var[str] = None
    format: Var[Literal["hex", "hexa", "rgba", "rgb", "hsl", "hsla"]] = None
    swatches: Var[list[str]] = None
    swatches_per_row: Var[int] = None
    with_picker: Var[bool] = None
    size: Var[str | int] = None
    full_width: Var[bool] = None
    focusable: Var[bool] = None
    name: Var[str] = None
    alpha_label: Var[str] = None
    hue_label: Var[str] = None
    saturation_label: Var[str] = None

    on_change: EventHandler[lambda value: [value]] = None
    on_change_end: EventHandler[lambda value: [value]] = None
    on_color_swatch_click: EventHandler[lambda color: [color]] = None


class AlphaSlider(MantineLayoutComponentBase):
    """Mantine AlphaSlider component — alpha transparency slider.

    https://mantine.dev/core/alpha-slider/
    """

    tag = "AlphaSlider"

    _rename_props = {
        "on_change_end": "onChangeEnd",
        "on_scrub_end": "onScrubEnd",
        "on_scrub_start": "onScrubStart",
    }

    value: Var[int | float] = None
    color: Var[str] = None
    size: Var[str | int] = None
    focusable: Var[bool] = None

    on_change: EventHandler[lambda value: [value]] = None
    on_change_end: EventHandler[lambda value: [value]] = None
    on_scrub_start: EventHandler[rx.event.no_args_event_spec] = None
    on_scrub_end: EventHandler[rx.event.no_args_event_spec] = None


class HueSlider(MantineLayoutComponentBase):
    """Mantine HueSlider component — hue color picker slider.

    https://mantine.dev/core/hue-slider/
    """

    tag = "HueSlider"

    _rename_props = {
        "on_change_end": "onChangeEnd",
        "on_scrub_end": "onScrubEnd",
        "on_scrub_start": "onScrubStart",
    }

    value: Var[int | float] = None
    size: Var[str | int] = None
    focusable: Var[bool] = None

    on_change: EventHandler[lambda value: [value]] = None
    on_change_end: EventHandler[lambda value: [value]] = None
    on_scrub_start: EventHandler[rx.event.no_args_event_spec] = None
    on_scrub_end: EventHandler[rx.event.no_args_event_spec] = None
