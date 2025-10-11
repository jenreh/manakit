from collections.abc import Callable

import reflex as rx

from manakit_assistant.backend.models import Suggestion
from manakit_assistant.components.composer import ComposerComponent
from manakit_assistant.components.message import MessageComponent
from manakit_assistant.components.threadlist import ThreadList
from manakit_assistant.state.thread_state import (
    Message,
    MessageType,
    ThreadListState,
    ThreadState,
)


class Assistant:
    @staticmethod
    def suggestion(
        prompt: str,
        icon: str | None = None,
        update_prompt: Callable | None = None,
        **props,
    ) -> rx.Component:
        """Component to display a suggestion."""

        on_click_handler = update_prompt(prompt) if update_prompt else None

        return rx.button(
            rx.cond(icon, rx.icon(icon), None),
            prompt,
            size="2",
            variant="soft",
            radius="large",
            on_click=on_click_handler,
            **props,
        )

    @staticmethod
    def empty(
        welcome_message: str,
        **props,
    ) -> rx.Component:
        """Component to display when there are no messages."""
        return rx.vstack(
            rx.text(welcome_message, size="8", margin_bottom="0.5em"),
            rx.cond(
                ThreadState.suggestions,
                rx.flex(
                    rx.foreach(
                        ThreadState.suggestions,
                        lambda suggestion: Assistant.suggestion(
                            prompt=suggestion.prompt,
                            icon=suggestion.icon,
                            update_prompt=ThreadState.update_prompt,
                        ),
                    ),
                    spacing="4",
                    width="100%",
                    direction="row",
                    wrap="wrap",
                ),
                None,
            ),
            **props,
        )

    @staticmethod
    def messages(
        with_scroll_to_bottom: bool = True,
        **props,
    ) -> rx.Component:
        """Component to display messages in the thread."""

        if ThreadState.messages is None:
            messages = [Message(text="👋 Hi!", type=MessageType.ASSISTANT)]
        else:
            messages = ThreadState.messages

        return rx.fragment(
            rx.auto_scroll(
                rx.foreach(
                    messages,
                    lambda message: MessageComponent.render_message(message),
                ),
                rx.spacer(
                    id="scroll-anchor",
                    display="hidden",
                    min_height="44px",
                    wrap="nowrap",
                ),
                id="messages-scroll-area",
                **props,
            ),
            rx.cond(
                with_scroll_to_bottom,
                MessageComponent.scroll_to_bottom(),
                None,
            ),
        )

    @staticmethod
    def composer(
        with_attachments: bool = False,
        with_model_chooser: bool = False,
        with_tools: bool = False,
        with_clear: bool = True,
        **props,
    ) -> rx.Component:
        return rx.vstack(
            ComposerComponent.input(),
            rx.hstack(
                rx.hstack(
                    ComposerComponent.choose_model(show=with_model_chooser),
                ),
                rx.hstack(
                    ComposerComponent.tools(
                        show=with_tools and ThreadState.current_model_supports_tools
                    ),
                    ComposerComponent.add_attachment(show=with_attachments),
                    ComposerComponent.clear(show=with_clear),
                    ComposerComponent.submit(),
                    width="100%",
                    justify="end",
                    align="center",
                    spacing="4",
                ),
                padding="0 12px 12px 12px",
                width="100%",
                align="center",
            ),
            **props,
        )

    @staticmethod
    def thread(
        welcome_message: str = "",
        suggestions: list[Suggestion] | None = None,
        with_attachments: bool = False,
        with_clear: bool = True,
        with_model_chooser: bool = True,
        with_scroll_to_bottom: bool = False,
        with_thread_list: bool = False,
        with_tools: bool = False,
        **props,
    ) -> rx.Component:
        if suggestions is not None:
            ThreadState.suggestions = suggestions

        if with_thread_list:
            ThreadState.with_thread_list = with_thread_list

        return rx.flex(
            rx.cond(
                ThreadState.messages,
                Assistant.messages(
                    with_scroll_to_bottom=with_scroll_to_bottom,
                    width="100%",
                    margin_bottom="-1em",
                    flex_grow=1,
                    justify_content="start",
                ),
                Assistant.empty(
                    welcome_message=welcome_message,
                    suggestions=suggestions,
                    width="100%",
                    max_width="880px",
                    margin_left="auto",
                    margin_right="auto",
                    margin_bottom="2em",
                    flex_grow=1,
                    justify_content="flex-end",
                ),
            ),
            Assistant.composer(
                with_attachments=with_attachments,
                with_tools=with_tools,
                with_model_chooser=with_model_chooser,
                with_clear=with_clear,
                # styling
                border=rx.color_mode_cond(
                    light=f"1px solid {rx.color('gray', 9)}",
                    dark=f"1px solid {rx.color('white', 7, alpha=True)}",
                ),
                box_shadow=rx.color_mode_cond(
                    light="0 1px 10px -0.5px rgba(0, 0, 0, 0.1)",
                    dark="0 1px 10px -0.5px rgba(0.8, 0.8, 0.8, 0.1)",
                ),
                border_radius="10px",
                background_color=rx.color_mode_cond(
                    light=rx.color("white", 9, alpha=True),
                    dark=rx.color("white", 2, alpha=False),
                ),
                width="100%",
                max_width="880px",
                margin_left="auto",
                margin_right="auto",
                margin_top="1em",
                spacing="0",
                flex_shrink=0,
                z_index=1000,
                on_mount=ThreadState.load_available_mcp_servers,
            ),
            **props,
        )

    @staticmethod
    def thread_list(
        *items,
        with_footer: bool = False,
        default_model: str | None = None,
        **props,
    ) -> rx.Component:
        if default_model:
            ThreadListState.default_model = default_model

        return rx.flex(
            rx.flex(
                ThreadList.header(
                    title="Neuer Chat",
                    margin_bottom="1.5em",
                    flex_shrink=0,
                ),
                ThreadList.list(
                    flex_grow=1,
                    min_height="60px",
                ),
                rx.cond(
                    with_footer,
                    ThreadList.footer(
                        *items,
                        flex_shrink=0,
                        min_height="48px",
                    ),
                    None,
                ),
                flex_direction=["column"],
                width="100%",
                height="100%",
                overflow="hidden",
            ),
            overflow="hidden",
            **props,
        )
