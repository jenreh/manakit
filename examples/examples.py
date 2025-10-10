"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import logging

import reflex as rx
import reflex_enterprise as rxe

from examples.pages.action_icon_examples import action_icon_examples
from examples.pages.autocomplete_examples import autocomplete_examples
from examples.pages.button_examples import button_examples
from examples.pages.combobox_examples import combobox_examples
from examples.pages.date_input_examples import date_input_examples_page
from examples.pages.input_examples import form_inputs_showcase
from examples.pages.json_input_examples import json_input_examples
from examples.pages.nav_link_examples import nav_link_examples
from examples.pages.nprogress_examples import nprogress_examples_page
from examples.pages.number_formatter_examples import number_formatter_examples
from examples.pages.number_input_examples import number_input_examples_page
from examples.pages.password_input_examples import password_input_examples_page
from examples.pages.select_examples import select_examples
from examples.pages.textarea_examples import textarea_examples_page
from examples.pages.tiptap_examples import tiptap_page

logging.basicConfig(level=logging.DEBUG)


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
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
            rx.text.strong("Explore the MantineUI examples:", size="3"),
            rx.list.unordered(
                rx.list.item(rx.link("Text Inputs", href="/inputs")),
                rx.list.item(rx.link("Password Input", href="/password")),
                rx.list.item(rx.link("Date Input", href="/date")),
                rx.list.item(rx.link("Number Input", href="/number")),
                rx.list.item(rx.link("Textarea", href="/textarea")),
                rx.list.item(rx.link("Select", href="/select")),
                rx.list.item(rx.link("Autocomplete", href="/autocomplete")),
                rx.list.item(rx.link("Combobox", href="/combobox")),
                rx.list.item(rx.link("Rich Text Editor (Tiptap)", href="/tiptap")),
                rx.list.item(rx.link("Navigation Progress", href="/nprogress")),
                rx.list.item(rx.link("Action Icon (Group demo)", href="/action-icon")),
                rx.list.item(rx.link("Button", href="/button")),
                rx.list.item(rx.link("Json Input", href="/json-input")),
                rx.list.item(rx.link("Nav Link", href="/nav-link")),
                rx.list.item(rx.link("Number Formatter", href="/number-formatter")),
            ),
            spacing="2",
            justify="center",
            min_height="85vh",
        ),
    )


app = rxe.App()
app.add_page(index)

app.add_page(password_input_examples_page, title="Password Input", route="/password")
app.add_page(date_input_examples_page, title="Date Input", route="/date")
app.add_page(number_input_examples_page, title="Number Input", route="/number")
app.add_page(textarea_examples_page, title="Textarea", route="/textarea")
app.add_page(form_inputs_showcase, title="Inputs", route="/inputs")
app.add_page(nprogress_examples_page, title="Navigation Progress", route="/nprogress")
app.add_page(tiptap_page, title="Rich Text Editor", route="/tiptap")
app.add_page(select_examples, title="Select", route="/select")
app.add_page(autocomplete_examples, title="Autocomplete", route="/autocomplete")
app.add_page(combobox_examples, title="Combobox", route="/combobox")
app.add_page(action_icon_examples, title="Action Icon", route="/action-icon")
app.add_page(button_examples, title="Button", route="/button")
app.add_page(json_input_examples, title="Json Input", route="/json-input")
app.add_page(nav_link_examples, title="Nav Link", route="/nav-link")
app.add_page(
    number_formatter_examples,
    title="Number Formatter",
    route="/number-formatter",
)
