import reflex as rx


def header(
    text: str,
    indent: bool = False,
) -> rx.Component:
    return rx.box(
        rx.color_mode_cond(
            light=rx.heading(
                text,
                size="5",
                class_name="text-black",
            ),
            dark=rx.heading(
                text,
                size="5",
                class_name="text-white",
            ),
        ),
        class_name=(
            "fixed top-0 z-[1000] w-full "
            "border-b border-gray-300 dark:border-neutral-700 "
            "bg-gray-50 dark:bg-neutral-800 "
            "p-3 pl-8 transition-colors duration-300"
        ),
        margin_left=rx.cond(indent, "0", "-32px"),
    )
