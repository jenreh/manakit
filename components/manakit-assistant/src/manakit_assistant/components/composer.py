import reflex as rx

import manakit_mantine as mn
from manakit_assistant.components.composer_key_handler import keyboard_shortcuts
from manakit_assistant.components.tools_modal import tools_popover
from manakit_assistant.state.thread_state import ThreadState


def render_model_option(model: dict) -> rx.Component:
    return rx.hstack(
        rx.cond(
            model.icon,
            rx.image(
                src=rx.color_mode_cond(
                    light=f"/icons/{model.icon}.svg",
                    dark=f"/icons/{model.icon}_dark.svg",
                ),
                width="13px",
                margin_right="8px",
            ),
            None,
        ),
        rx.text(model.text),
        align="center",
        spacing="0",
    )


class ComposerComponent:
    """Composer component for sending messages in a thread."""

    @staticmethod
    def input(placeholder: str = "Frage etwas...") -> rx.Component:
        return mn.textarea(
            id="composer-area",
            name="composer_prompt",
            placeholder=placeholder,
            value=ThreadState.prompt,
            autosize=True,
            variant="unstyled",
            min_rows=1,
            max_rows=8,
            custom_attrs={
                "style": {
                    "padding": "6px 12px",
                }
            },
            width="100%",
            on_change=ThreadState.set_prompt_direct,
        )

    @staticmethod
    def submit() -> rx.Component:
        return rx.fragment(
            rx.button(
                rx.icon("arrow-right", size=18),
                id="composer-submit",
                name="composer_submit",
                on_click=ThreadState.submit_message,
                loading=ThreadState.processing,
            ),
            keyboard_shortcuts(),
        )

    @staticmethod
    def add_attachment(show: bool = False) -> rx.Component | None:
        if not show:
            return None

        return rx.tooltip(
            rx.button(
                rx.icon("paperclip", size=18),
                rx.text("2 files", size="1", color="gray.2"),
                id="composer-attachment",
                variant="ghost",
                padding="8px",
                access_key="s",
            ),
            content="Manage Attachments…",
        )

    @staticmethod
    def choose_model(show: bool = False) -> rx.Component | None:
        if not show:
            return None

        return rx.cond(
            ThreadState.ai_models,
            mn.rich_select(
                mn.rich_select.map(
                    ThreadState.ai_models,
                    renderer=render_model_option,
                    value=lambda model: model.id,
                ),
                placeholder="Wähle ein Modell",
                value=ThreadState.selected_model,
                on_change=ThreadState.set_selected_model,
                name="model-select",
                width="252px",
                position="top",
            ),
            None,
        )

    @staticmethod
    def tools(show: bool = False) -> rx.Component:
        """Render tools button with conditional visibility."""
        return rx.cond(
            show,
            rx.hstack(
                tools_popover(),
                spacing="1",
                align="center",
            ),
            rx.fragment(),  # Empty fragment when hidden
        )

    @staticmethod
    def clear(show: bool = True) -> rx.Component | None:
        if not show:
            return None

        return rx.tooltip(
            rx.button(
                rx.icon("paintbrush", size=17),
                variant="ghost",
                padding="8px",
                on_click=ThreadState.clear,
            ),
            content="Chatverlauf löschen",
        )
