import reflex as rx
from knai_assistant.components.tools_modal import tools_popover
from knai_assistant.state.thread_state import AIModel, ThreadState


def render_model_option(model: AIModel) -> rx.Component:
    return rx.select.item(
        rx.hstack(
            rx.cond(
                model.icon,
                rx.image(
                    src=rx.color_mode_cond(
                        light=f"/icons/{model.icon}.svg",
                        dark=f"/icons/{model.icon}_dark.svg",
                    ),
                    width="13px",
                ),
                None,
            ),
            rx.text(model.text),
            align="center",
        ),
        value=model.id,
    )


class ComposerComponent:
    """Composer component for sending messages in a thread."""

    @staticmethod
    def input(placeholder: str = "Frage etwas...") -> rx.Component:
        return rx.text_area(
            id="composer-area",
            name="composer_prompt",
            placeholder=placeholder,
            value=ThreadState.prompt,
            # Stil
            border="0",
            outline="none",
            variant="soft",
            background_color=rx.color("white", 1, alpha=False),
            padding="9px 3px",
            autocorrect="on",
            size="3",
            # Layout
            width="100%",
            min_height="24px",
            max_height="244px",
            resize="none",
            rows="1",
            # Ereignisse
            on_change=ThreadState.update_prompt,
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
            rx.script(src="/js/shortcuts.js"),
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
            rx.select.root(
                rx.select.trigger(
                    placeholder="Wähle ein Modell",
                    radius="large",
                    width="210px",
                    margin_top="-3px",
                ),
                rx.select.content(
                    rx.foreach(
                        ThreadState.ai_models,
                        render_model_option,
                    ),
                    position="popper",
                    side="top",
                ),
                name="model-select",
                value=ThreadState.selected_model,
                radius="large",
                size="2",
                on_change=ThreadState.set_selected_model,
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
