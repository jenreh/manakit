import reflex as rx
from reflex.components.radix.themes.layout.box import Box

from appkit_imagecreator.components.options_ui import (
    advanced_options,
    enhance_prompt_checkbox,
    generate_button,
    output_selector,
    prompt_input,
    size_selector,
    style_selector,
)


def sidebar() -> Box:
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.vstack(
                    prompt_input(),
                    size_selector(),
                    output_selector(),
                    style_selector(),
                    enhance_prompt_checkbox(),
                    advanced_options(),
                    width="100%",
                    overflow_y="auto",
                    align="start",
                    padding="1em",
                    spacing="6",
                ),
                overflow_y="auto",
                flex="1",
                height="100%",
                width="100%",
            ),
            generate_button(),
            width="100%",
            height="100%",
            spacing="0",
        ),
        display=["none", "none", "none", "block"],
        width=["100%", "100%", "100%", "375px", "450px"],
        height="100vh",
        position="sticky",
        top="0px",
        left="0px",
        bg=rx.color("gray", 2),
        border_right=f"1px solid {rx.color('gray', 5)}",
    )
