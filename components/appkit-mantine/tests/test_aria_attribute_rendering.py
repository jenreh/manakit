"""Render-level tests for hyphenated DOM attributes (aria-label, data-disabled).

Reflex camelCases every prop name in ``Tag.add_props`` before applying
``_rename_props``, so declared props like ``aria_label`` used to reach the DOM
as invalid ``ariaLabel``. ``MantineComponentBase._render`` restores the
hyphenated names on the rendered tag; these tests assert the emitted props.
"""

from __future__ import annotations

import reflex as rx

import appkit_mantine as mn


def _props(component: rx.Component) -> list[str]:
    return component.render().get("props", [])


def _assert_hyphenated(props: list[str], attribute: str) -> None:
    """Assert the attribute is emitted quoted and no camelCase leak remains."""
    assert any(entry.startswith(f'"{attribute}":') for entry in props), props
    camel = "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(attribute.split("-"))
    )
    assert not any(entry.startswith(f"{camel}:") for entry in props), props


def test_text_input_aria_label_renders_hyphenated() -> None:
    props = _props(mn.text_input(aria_label="Search"))
    _assert_hyphenated(props, "aria-label")
    assert '"aria-label":"Search"' in props


def test_button_aria_label_and_data_disabled() -> None:
    props = _props(mn.button("Save", aria_label="Save form", data_disabled=True))
    _assert_hyphenated(props, "aria-label")
    _assert_hyphenated(props, "data-disabled")


def test_action_icon_aria_label() -> None:
    props = _props(mn.action_icon(aria_label="Delete row"))
    _assert_hyphenated(props, "aria-label")


def test_drawer_close_button_aria_label() -> None:
    props = _props(mn.drawer.close_button(aria_label="Close drawer"))
    _assert_hyphenated(props, "aria-label")


def test_modal_close_button_default_aria_label() -> None:
    props = _props(mn.modal.close_button())
    assert '"aria-label":"Close modal"' in props


def test_nav_link_aria_label_via_special_attributes() -> None:
    props = _props(mn.nav_link(label="Home", aria_label="Home link"))
    _assert_hyphenated(props, "aria-label")


def test_aria_label_accepts_state_var() -> None:
    class AriaState(rx.State):
        label: str = "dynamic"

    props = _props(mn.text_input(aria_label=AriaState.label))
    assert any(entry.startswith('"aria-label":') for entry in props), props


def test_custom_attrs_wins_over_declared_prop() -> None:
    props = _props(
        mn.text_input(
            aria_label="from prop",
            custom_attrs={"aria-label": "from custom_attrs"},
        )
    )
    aria_entries = [e for e in props if e.startswith('"aria-label":')]
    assert aria_entries == ['"aria-label":"from custom_attrs"'], props


def test_render_without_aria_props_is_untouched() -> None:
    props = _props(mn.text_input(placeholder="Name"))
    assert any(entry.startswith("placeholder:") for entry in props), props
    assert not any("aria" in entry for entry in props), props
