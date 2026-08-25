"""Mantine input components — public API facade.

The component classes live in thematic submodules:

- :mod:`appkit_mantine.inputs_core` — Input + Input.* sub-components
- :mod:`appkit_mantine.inputs_text` — TextInput, PasswordInput, Textarea,
  JsonInput, MaskInput, PinInput
- :mod:`appkit_mantine.inputs_number` — NumberInput, Rating, AngleSlider
- :mod:`appkit_mantine.inputs_color` — ColorInput, ColorPicker, AlphaSlider,
  HueSlider
- :mod:`appkit_mantine.inputs_misc` — TagsInput, NativeSelect, FileInput,
  Fieldset, Chip

This module re-exports everything so existing ``appkit_mantine.inputs``
imports keep working, and defines the ``form``/``chip`` namespaces and the
factory function aliases.
"""

from __future__ import annotations

import reflex as rx

from appkit_mantine.date import DateInput
from appkit_mantine.inputs_color import (
    AlphaSlider,
    ColorInput,
    ColorPicker,
    HueSlider,
)
from appkit_mantine.inputs_core import (
    Input,
    InputClearButton,
    InputDescription,
    InputError,
    InputLabel,
    InputPlaceholder,
    InputWrapper,
)
from appkit_mantine.inputs_misc import (
    Chip,
    ChipGroup,
    Fieldset,
    FileInput,
    NativeSelect,
    TagsInput,
)
from appkit_mantine.inputs_number import AngleSlider, NumberInput, Rating
from appkit_mantine.inputs_text import (
    IMASK_VERSION,
    JsonInput,
    MaskInput,
    PasswordInput,
    PinInput,
    Textarea,
    TextInput,
)

__all__ = [
    "IMASK_VERSION",
    "AlphaSlider",
    "AngleSlider",
    "Chip",
    "ChipGroup",
    "ChipNamespace",
    "ColorInput",
    "ColorPicker",
    "DateInput",
    "Fieldset",
    "FileInput",
    "HueSlider",
    "Input",
    "InputClearButton",
    "InputDescription",
    "InputError",
    "InputLabel",
    "InputNamespace",
    "InputPlaceholder",
    "InputWrapper",
    "JsonInput",
    "MaskInput",
    "NativeSelect",
    "NumberInput",
    "PasswordInput",
    "PinInput",
    "Rating",
    "TagsInput",
    "TextInput",
    "Textarea",
    "alpha_slider",
    "angle_slider",
    "chip",
    "color_input",
    "color_picker",
    "fieldset",
    "file_input",
    "form",
    "hue_slider",
    "input_wrapper",
    "json_input",
    "masked_input",
    "native_select",
    "number_input",
    "password_input",
    "pin_input",
    "rating",
    "tags_input",
    "text_input",
    "textarea",
]


# ============================================================================
# Convenience Functions
# ============================================================================


class ChipNamespace(rx.ComponentNamespace):
    """Namespace for Chip components."""

    __call__ = staticmethod(Chip.create)
    group = staticmethod(ChipGroup.create)


class InputNamespace(rx.ComponentNamespace):
    """Namespace for input components."""

    input = staticmethod(Input.create)
    text = staticmethod(TextInput.create)
    password = staticmethod(PasswordInput.create)
    number = staticmethod(NumberInput.create)
    masked = staticmethod(MaskInput.create)
    textarea = staticmethod(Textarea.create)
    json = staticmethod(JsonInput.create)
    date = staticmethod(DateInput.create)
    tags = staticmethod(TagsInput.create)

    # Sub-components
    wrapper = staticmethod(InputWrapper.create)
    label = staticmethod(InputLabel.create)
    description = staticmethod(InputDescription.create)
    error = staticmethod(InputError.create)
    placeholder = staticmethod(InputPlaceholder.create)
    clear_button = staticmethod(InputClearButton.create)


form = InputNamespace()


# Export convenience functions for direct access
alpha_slider = AlphaSlider.create
angle_slider = AngleSlider.create
chip = ChipNamespace()
color_input = ColorInput.create
color_picker = ColorPicker.create
fieldset = Fieldset.create
file_input = FileInput.create
hue_slider = HueSlider.create
json_input = JsonInput.create
masked_input = MaskInput.create
native_select = NativeSelect.create
number_input = NumberInput.create
password_input = PasswordInput.create
pin_input = PinInput.create
rating = Rating.create
tags_input = TagsInput.create
text_input = TextInput.create
textarea = Textarea.create
input_wrapper = InputWrapper.create
