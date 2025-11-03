from collections.abc import Callable

import reflex as rx


def collabsible(
    *children: rx.Component,
    title: str,
    info_text: str = "",
    show_condition: bool = True,
    expanded: bool = False,
    on_toggle: Callable | None = None,
    **props,
) -> rx.Component:
    """
    Erstellt eine Collapsible Komponente mit beliebig vielen Child-Komponenten

    Args:
        *children: Beliebige Anzahl von Reflex Komponenten als positionale Argumente
        title: Titel der Collapsible Sektion
        info_text: Info-Text rechts neben dem Titel
        show_condition: Bedingung, wann die Komponente angezeigt wird
        expanded: Zustand, ob die Komponente erweitert ist
        on_toggle: Event handler für das Umschalten
        **props: Zusätzliche Props für das Container-Element
    """
    return rx.vstack(
        # Collapsible header - klickbarer Bereich
        rx.vstack(
            rx.hstack(
                rx.icon(
                    rx.cond(
                        expanded,
                        "chevron-down",
                        "chevron-right",
                    ),
                    size=16,
                ),
                rx.text(
                    title,
                    size="1",
                    font_weight="medium",
                    color=rx.color("gray", 11),
                    flex_grow="1",
                ),
                rx.text(
                    info_text,
                    size="1",
                    color=rx.color("gray", 9),
                    text_align="right",
                    width="40%",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            on_click=on_toggle,
            padding="8px",
            width="100%",
            _hover={"background_color": rx.color("gray", 2)},
        ),
        # Expandierbarer Inhalt - alle Children werden in einem vstack angeordnet
        rx.cond(
            expanded,
            *children,  # Alle übergebenen Komponenten werden hier eingefügt
        ),
        # Container Styling
        spacing="3",
        width="calc(90% + 18px)",
        background_color=rx.color("gray", 1),
        border=f"1px solid {rx.color('gray', 6)}",
        border_radius="8px",
        # Animationen
        opacity=rx.cond(show_condition, "1", "0"),
        transform=rx.cond(show_condition, "translateY(0)", "translateY(-20px)"),
        height=rx.cond(show_condition, "auto", "0"),
        max_height=rx.cond(show_condition, "500px", "0"),
        padding=rx.cond(show_condition, "3px", "0"),
        margin_top=rx.cond(show_condition, "16px", "-16px"),
        overflow="hidden",
        pointer_events=rx.cond(show_condition, "auto", "none"),
        # transition="all 1s ease-out",
        **props,
    )
