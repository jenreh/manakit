"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import logging

import reflex as rx

from reflex_mantine.pages.date_input_examples import date_input_examples_page
from reflex_mantine.pages.input_examples import form_inputs_showcase
from reflex_mantine.pages.nprogress_examples import nprogress_examples_page
from reflex_mantine.pages.number_input_examples import number_input_examples_page
from reflex_mantine.pages.password_input_examples import password_input_examples_page
from reflex_mantine.pages.textarea_examples import textarea_examples_page
from reflex_mantine.pages.tiptap_examples import tiptap_page
from rxconfig import config

logging.basicConfig(level=logging.DEBUG)


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link("Password Input", href="/password"),
            rx.link("Date Input", href="/date"),
            rx.link("Number Input", href="/number"),
            rx.link("Textarea", href="/textarea"),
            rx.link("Inputs Showcase", href="/inputs"),
            rx.link("Navigation Progress", href="/nprogress"),
            rx.link("Rich Text Editor (Tiptap)", href="/tiptap"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)

app.add_page(password_input_examples_page, title="Password Input", route="/password")
app.add_page(date_input_examples_page, title="Date Input", route="/date")
app.add_page(number_input_examples_page, title="Number Input", route="/number")
app.add_page(textarea_examples_page, title="Textarea", route="/textarea")
app.add_page(form_inputs_showcase, title="Inputs", route="/inputs")
app.add_page(nprogress_examples_page, title="Navigation Progress", route="/nprogress")
app.add_page(tiptap_page, title="Rich Text Editor", route="/tiptap")
