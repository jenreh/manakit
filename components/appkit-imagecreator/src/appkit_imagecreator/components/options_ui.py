import reflex as rx

from appkit_imagecreator.states import GeneratorState, OptionsState


def prompt_input() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text("Generator", size="3"),
            rx.select.root(
                rx.select.trigger(
                    placeholder="Modell auswählen",
                    radius="large",
                ),
                rx.select.content(
                    rx.foreach(
                        OptionsState.generators,
                        lambda model: rx.select.item(
                            rx.text(model["label"]),
                            value=model["id"],
                        ),
                    ),
                    position="popper",
                    side="top",
                ),
                name="model-select",
                value=OptionsState.generator,
                radius="large",
                size="2",
                on_change=OptionsState.set_generator,
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.hstack(
            rx.icon("type", size=17, color=rx.color("green", 9)),
            rx.text("Prompt", size="3"),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    OptionsState.prompt,
                    rx.icon(
                        "eraser",
                        size=20,
                        color=rx.color("gray", 10),
                        cursor="pointer",
                        _hover={"opacity": "0.8"},
                        on_click=OptionsState.set_prompt(""),
                    ),
                ),
                rx.tooltip(
                    rx.box(
                        rx.icon(
                            "dices",
                            size=20,
                            color=rx.color("gray", 10),
                            cursor="pointer",
                            _hover={"opacity": "0.8"},
                            on_click=OptionsState.randomize_prompt,
                        ),
                    ),
                    content="Zufälliger Prompt",
                ),
                spacing="4",
                align="center",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.text_area(
            placeholder="Was möchtest du sehen?",
            width="100%",
            rows="4",
            resize="vertical",
            size="3",
            value=OptionsState.prompt,
            on_change=OptionsState.set_prompt,
        ),
        width="100%",
    )


def _create_arrow_icon(
    direction: str = "",
    top: str = "",
    left: str = "",
    right: str = "",
    bottom: str = "",
) -> rx.Component:
    return rx.icon(
        direction,
        size=17,
        color=rx.color("gray", 10),
        position="absolute",
        top=top,
        left=left,
        right=right,
        bottom=bottom,
    )


def size_selector() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("scan", size=17, color=rx.color("orange", 9)),
            rx.text("Dimensionen", size="3"),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.vstack(
            rx.slider(
                min=0,
                max=(OptionsState.dimensions).length() - 1,
                step=1,
                size="1",
                default_value=OptionsState.slider_tick,
                on_change=OptionsState.set_tick,
                on_blur=OptionsState.set_hover(False),
                on_mouse_enter=OptionsState.set_hover(True),
                on_mouse_leave=OptionsState.set_hover(False),
            ),
            rx.hstack(
                rx.icon(
                    "rectangle-horizontal",
                    size=22,
                    color=rx.color("gray", 9),
                ),
                rx.center(
                    rx.flex(
                        rx.text(
                            OptionsState.dimensions_str,
                            size="2",
                            justify="center",
                            align="center",
                        ),
                        _create_arrow_icon("arrow-up-left", top="2.5px", left="2.5px"),
                        _create_arrow_icon(
                            "arrow-up-right", top="2.5px", right="2.5px"
                        ),
                        _create_arrow_icon(
                            "arrow-down-left",
                            bottom="2.5px",
                            left="2.5px",
                        ),
                        _create_arrow_icon(
                            "arrow-down-right",
                            bottom="2.5px",
                            right="2.5px",
                        ),
                        width=OptionsState.dimensions[OptionsState.slider_tick][0] // 8,
                        height=OptionsState.dimensions[OptionsState.slider_tick][1]
                        // 8,
                        bg=rx.color("gray", 7),
                        padding="2.5px",
                        justify="center",
                        align="center",
                        position="relative",
                        transition="all 0.1s ease",
                        border=f"1px solid {rx.color('gray', 5)}",
                        box_shadow="0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",  # noqa: E501
                        style={
                            "transition": (
                                "opacity 0.3s ease-out, transform 0.3s "
                                "ease-out, visibility 0.3s ease-out"
                            ),
                            "opacity": rx.cond(OptionsState.hover, "1", "0"),
                            "visibility": rx.cond(
                                OptionsState.hover, "visible", "hidden"
                            ),
                            "transform": rx.cond(
                                OptionsState.hover, "scale(1)", "scale(0)"
                            ),
                        },
                    ),
                    position="absolute",
                    transform="translate(0%, 45%)",
                    width="100%",
                    z_index=rx.cond(OptionsState.hover, "500", "0"),
                ),
                rx.text(
                    OptionsState.dimensions_str,
                    size="2",
                    style={
                        "transition": (
                            "opacity 0.15s ease-out, visibility 0.15s ease-out"
                        ),
                        "visibility": rx.cond(OptionsState.hover, "hidden", "visible"),
                        "opacity": rx.cond(OptionsState.hover, "0", "1"),
                    },
                ),
                rx.icon(
                    "rectangle-vertical",
                    size=22,
                    color=rx.color("gray", 9),
                ),
                position="relative",
                justify="between",
                align="center",
                width="100%",
            ),
            width="100%",
        ),
        width="100%",
    )


def output_selector() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("image", size=17, color=rx.color("crimson", 9)),
            rx.text("Anzahl Bilder", size="3"),
            rx.spacer(),
            rx.text(f"{OptionsState.num_outputs}", size="3"),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.slider(
            min=1,
            max=4,
            step=1,
            size="1",
            default_value=OptionsState.num_outputs,
            on_change=OptionsState.set_num_outputs,
        ),
        width="100%",
    )


def _style_preview(style_preset: list) -> rx.Component:
    box_style = {
        "width": "110px",
        "height": "110px",
        "cursor": "pointer",
        "transition": "all 0.2s ease",
        "background": rx.color("accent", 9),
    }

    img_style = {
        "width": "100%",
        "height": "auto",
        "decoding": "async",
        "loading": "lazy",
        "transition": "all 0.2s ease",
    }

    return rx.cond(
        style_preset[0] == OptionsState.selected_style,
        rx.tooltip(
            rx.box(
                rx.image(
                    src=style_preset[1]["path"],
                    style=img_style,
                    transform="scale(0.875)",
                ),
                style=box_style,
                on_click=OptionsState.set_selected_style(""),
            ),
            content=style_preset[0],
        ),
        rx.tooltip(
            rx.box(
                rx.image(
                    src=style_preset[1]["path"],
                    style=img_style,
                ),
                style=box_style,
                on_click=OptionsState.set_selected_style(style_preset[0]),
            ),
            content=style_preset[0],
        ),
    )


def style_selector() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("palette", size=17, color=rx.color("indigo", 9)),
            rx.text("Stil", size="3"),
            rx.spacer(),
            rx.cond(
                OptionsState.selected_style,
                rx.hstack(
                    rx.text(f"[ {OptionsState.selected_style} ]", size="3"),
                    rx.icon(
                        "eraser",
                        size=20,
                        color=rx.color("gray", 10),
                        cursor="pointer",
                        _hover={"opacity": "0.8"},
                        on_click=OptionsState.set_selected_style(""),
                    ),
                    spacing="4",
                    align="center",
                ),
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.scroll_area(
            rx.hstack(
                rx.foreach(OptionsState.styles_preset, _style_preview),
                width="100%",
                align="center",
                padding_bottom="15px",
            ),
            scrollbars="horizontal",
            height="100%",
            width="100%",
            type="always",
        ),
        width="100%",
    )


def _negative_prompt() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("type", size=17, color=rx.color("red", 9)),
            rx.text("Negativer Prompt", size="3"),
            rx.tooltip(
                rx.icon(
                    "info",
                    size=15,
                    color=rx.color("gray", 10),
                ),
                content="Dinge, die du im Bild vermeiden möchtest",
            ),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    OptionsState.negative_prompt,
                    rx.icon(
                        "eraser",
                        size=20,
                        color=rx.color("gray", 10),
                        cursor="pointer",
                        _hover={"opacity": "0.8"},
                        on_click=OptionsState.set_negative_prompt(""),
                    ),
                ),
                spacing="4",
                align="center",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.text_area(
            placeholder="Was möchtest du vermeiden?",
            width="100%",
            size="3",
            resize="vertical",
            value=OptionsState.negative_prompt,
            on_change=OptionsState.set_negative_prompt,
        ),
        width="100%",
    )


def _seed_input() -> rx.Component:
    return (
        rx.vstack(
            rx.hstack(
                rx.icon("sprout", size=17, color=rx.color("grass", 10)),
                rx.text("Seed", size="3"),
                rx.spacer(),
                rx.hstack(
                    rx.cond(
                        OptionsState.seed > 0,
                        rx.icon(
                            "eraser",
                            size=20,
                            color=rx.color("gray", 10),
                            cursor="pointer",
                            _hover={"opacity": "0.8"},
                            on_click=OptionsState.set_seed("0"),
                        ),
                    ),
                    spacing="4",
                    align="center",
                ),
                spacing="2",
                align="center",
                width="100%",
            ),
            rx.tooltip(
                rx.box(
                    rx.input(
                        type="number",
                        value=OptionsState.seed,
                        on_change=OptionsState.set_seed,
                        placeholder="0 (Auto)",
                        max_length=5,
                        width="100%",
                    ),
                    width="100%",
                ),
                content=(
                    "Eine Zahl, die die Zufälligkeit des Bildes bestimmt. "
                    "Verwende denselben Seed, um jedes Mal das gleiche "
                    "Ergebnis zu erhalten. 0 = Automatisch"
                ),
                side="right",
            ),
            spacing="2",
        ),
    )


def _advanced_options_grid() -> rx.Component:
    return rx.grid(
        _seed_input(),
        # _guidance_scale_input(),
        width="100%",
        columns="2",
        rows="2",
        spacing_x="5",
        spacing_y="5",
        justify="between",
        align="center",
    )


def advanced_options() -> rx.Component:
    return rx.vstack(
        rx.cond(
            OptionsState.advanced_options_open,
            rx.hstack(
                rx.icon(
                    "eye",
                    size=17,
                    color=rx.color("jade", 10),
                ),
                rx.text("Erweiterte Optionen", size="3"),
                align="center",
                spacing="2",
                width="100%",
                cursor="pointer",
                _hover={"opacity": "0.8"},
                on_click=OptionsState.set_advanced_options_open(False),
            ),
            rx.hstack(
                rx.icon(
                    "eye-off",
                    size=17,
                    color=rx.color("jade", 10),
                ),
                rx.text("Erweiterte Optionen", size="3"),
                align="center",
                spacing="2",
                width="100%",
                cursor="pointer",
                _hover={"opacity": "0.8"},
                on_click=OptionsState.set_advanced_options_open(True),
            ),
        ),
        rx.cond(
            OptionsState.advanced_options_open,
            rx.vstack(_negative_prompt(), _advanced_options_grid(), width="100%"),
        ),
        width="100%",
    )


def enhance_prompt_checkbox() -> rx.Component:
    return rx.hstack(
        rx.switch(
            checked=OptionsState.enhance_prompt,
            on_change=OptionsState.set_enhance_prompt,
            size="2",
        ),
        rx.text("Prompt automatisch verbessern", size="3"),
        rx.tooltip(
            rx.icon("info", size=15, color=rx.color("gray", 10)),
            content=(
                "Ein KI-Modell formuliert deinen Prompt automatisch um, "
                "um die Bildqualität zu verbessern. "
                "Dies kann etwas länger dauern."
            ),
        ),
        spacing="2",
        align="center",
        width="100%",
    )


def generate_button() -> rx.Component:
    return rx.box(
        rx.cond(
            ~GeneratorState.is_generating,
            rx.button(
                rx.icon("sparkles", size=18),
                "Generieren",
                size="3",
                cursor="pointer",
                width="100%",
                on_click=GeneratorState.generate_image,
            ),
            rx.button(
                rx.spinner(size="3"),
                "Abbrechen",
                size="3",
                width="100%",
                color_scheme="tomato",
                cursor="pointer",
                on_click=GeneratorState.cancel_generation,
            ),
        ),
        position="sticky",
        bottom="0",
        padding="1em",
        bg=rx.color("gray", 2),
        border_top=f"1px solid {rx.color('gray', 5)}",
        width="100%",
    )
