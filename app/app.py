"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import logging

import reflex as rx

from manakit_user.authentication.components.templates import (
    navbar_layout,
)

from app.components.navbar import app_navbar
from app.pages.examples.action_icon_examples import action_icon_examples
from app.pages.examples.autocomplete_examples import autocomplete_examples
from app.pages.examples.button_examples import button_examples
from app.pages.examples.date_input_examples import date_input_examples_page
from app.pages.examples.input_examples import form_inputs_showcase
from app.pages.examples.json_input_examples import json_input_examples
from app.pages.examples.multi_select_examples import multi_select_examples
from app.pages.examples.nav_link_examples import nav_link_examples
from app.pages.examples.nprogress_examples import nprogress_examples_page
from app.pages.examples.number_formatter_examples import number_formatter_examples
from app.pages.examples.number_input_examples import number_input_examples_page
from app.pages.examples.password_input_examples import password_input_examples_page
from app.pages.examples.scroll_area_examples import scroll_area_examples
from app.pages.examples.select_examples import select_examples
from app.pages.examples.table_examples import table_examples
from app.pages.examples.tags_input_examples import tags_input_examples
from app.pages.examples.textarea_examples import textarea_examples_page
from app.pages.examples.tiptap_examples import tiptap_page

logging.basicConfig(level=logging.DEBUG)


class State(rx.State):
    """The app state."""


@navbar_layout(
    route="/index",
    title="Home",
    description="A demo page for the ManaKit components",
    navbar=app_navbar(),
    with_header=False,
)
def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Welcome to ManaKit!", size="9"),
            rx.text(
                "A component library for ",
                rx.link("Reflex.dev", href="https://reflex.dev/", is_external=True),
                " based on ",
                rx.link("Mantine UI", href="https://mantine.dev/", is_external=True),
                margin_bottom="24px",
            ),
            # rx.separator(margin="12px"),
            rx.text.strong("Inputs:", size="3"),
            rx.list.unordered(
                rx.list.item(rx.link("Text Inputs", href="/inputs")),
                rx.list.item(rx.link("Password Input", href="/password")),
                rx.list.item(rx.link("Date Input", href="/date")),
                rx.list.item(rx.link("Number Input", href="/number")),
                rx.list.item(rx.link("Textarea", href="/textarea")),
                rx.list.item(rx.link("Json Input", href="/json-input")),
                rx.list.item(rx.link("Select", href="/select")),
                rx.list.item(rx.link("MultiSelect", href="/multi-select")),
                rx.list.item(rx.link("TagsInput", href="/tags-input")),
                rx.list.item(rx.link("Autocomplete", href="/autocomplete")),
                rx.list.item(rx.link("Rich Text Editor (Tiptap)", href="/tiptap")),
            ),
            rx.text.strong("Buttons:", size="3"),
            rx.list.unordered(
                rx.list.item(rx.link("Action Icon (Group demo)", href="/action-icon")),
                rx.list.item(rx.link("Button", href="/button")),
            ),
            rx.text.strong("Others:", size="3"),
            rx.list.unordered(
                rx.list.item(rx.link("Navigation Progress", href="/nprogress")),
                rx.list.item(rx.link("Nav Link", href="/nav-link")),
                rx.list.item(rx.link("Number Formatter", href="/number-formatter")),
                rx.list.item(rx.link("ScrollArea", href="/scroll-area")),
                rx.list.item(rx.link("Table", href="/table")),
            ),
            spacing="2",
            justify="center",
            margin_top="0",
        ),
    )


app = rx.App()
# app.add_page(index)

app.add_page(password_input_examples_page, title="Password Input", route="/password")
app.add_page(date_input_examples_page, title="Date Input", route="/date")
app.add_page(number_input_examples_page, title="Number Input", route="/number")
app.add_page(textarea_examples_page, title="Textarea", route="/textarea")
app.add_page(form_inputs_showcase, title="Inputs", route="/inputs")
app.add_page(nprogress_examples_page, title="Navigation Progress", route="/nprogress")
app.add_page(tiptap_page, title="Rich Text Editor", route="/tiptap")
app.add_page(select_examples, title="Select", route="/select")
app.add_page(multi_select_examples, title="MultiSelect", route="/multi-select")
app.add_page(tags_input_examples, title="TagsInput", route="/tags-input")
app.add_page(autocomplete_examples, title="Autocomplete", route="/autocomplete")
app.add_page(action_icon_examples, title="Action Icon", route="/action-icon")
app.add_page(button_examples, title="Button", route="/button")
app.add_page(json_input_examples, title="Json Input", route="/json-input")
app.add_page(nav_link_examples, title="Nav Link", route="/nav-link")
app.add_page(
    number_formatter_examples,
    title="Number Formatter",
    route="/number-formatter",
)
app.add_page(scroll_area_examples, title="ScrollArea", route="/scroll-area")
app.add_page(table_examples, title="Table", route="/table")
