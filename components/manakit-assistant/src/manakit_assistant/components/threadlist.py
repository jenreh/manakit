import reflex as rx

from manakit_assistant.state.thread_state import ThreadListState, ThreadModel


class ThreadList:
    @staticmethod
    def header(title: str = "Neuer Chat", **props) -> rx.Component:
        """Header component for the thread list."""
        return rx.flex(
            rx.tooltip(
                rx.button(
                    rx.text(title),
                    size="2",
                    margin_right="28px",
                    on_click=ThreadListState.create_thread(),
                    width="95%",
                ),
                content="Neuen Chat starten",
            ),
            direction="row",
            align="center",
            margin_top="9px",
            **props,
        )

    @staticmethod
    def footer(*items, **props) -> rx.Component:
        """Footer component for the thread list."""
        return rx.flex(
            *items,
            **props,
        )

    @staticmethod
    def thread_list_item(thread: ThreadModel) -> rx.Component:
        return rx.flex(
            rx.text(
                thread.title,
                size="2",
                white_space="nowrap",
                overflow="hidden",
                text_overflow="ellipsis",
                flex_grow="1",
                width="100px",
                min_width="0",
                title=thread.title,
            ),
            rx.tooltip(
                rx.button(
                    rx.icon(
                        "trash",
                        size=13,
                        stroke_width=1.5,
                    ),
                    variant="ghost",
                    size="1",
                    margin_left="0px",
                    margin_right="0px",
                    color_scheme="gray",
                    on_click=ThreadListState.delete_thread(thread.thread_id),
                ),
                content="Chat löschen",
                flex_shrink=0,
            ),
            on_click=ThreadListState.select_thread(thread.thread_id),
            flex_direction=["row"],
            margin_right="10px",
            margin_bottom="8px",
            padding="6px",
            align="center",
            border_radius="8px",
            background_color=rx.cond(
                thread.active,
                rx.color("accent", 3),
                rx.color("gray", 3),
            ),
            border=rx.cond(
                thread.active,
                f"1px solid {rx.color('gray', 5)}",
                "0",
            ),
            style={
                "_hover": {
                    "cursor": "pointer",
                    "background_color": rx.cond(
                        thread.active,
                        rx.color("accent", 4),
                        rx.color("gray", 6),
                    ),
                    "color": rx.cond(
                        thread.active,
                        rx.color("black", 9),
                        rx.color("white", 9),
                    ),
                    "opacity": "1",
                },
                "opacity": rx.cond(
                    thread.active,
                    "1",
                    "0.95",
                ),
            },
        )

    @staticmethod
    def list(**props) -> rx.Component:
        """List component for displaying threads."""
        return rx.scroll_area(
            rx.cond(
                ThreadListState.has_threads,
                rx.foreach(
                    ThreadListState.threads,
                    ThreadList.thread_list_item,
                ),
                rx.text(
                    "Keine Chats vorhanden.",
                    size="2",
                    white_space="nowrap",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    flex_grow="1",
                    min_width="0",
                    margin_right="10px",
                    margin_bottom="8px",
                    padding="6px",
                    align="center",
                ),
            ),
            scrollbars="vertical",
            padding_right="3px",
            type="auto",
            **props,
        )
