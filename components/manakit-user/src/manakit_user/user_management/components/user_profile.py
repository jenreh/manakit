import reflex as rx


def profile_state(
    label: str,
    default_value: bool = False,
) -> rx.Component:
    return rx.hstack(
        rx.text(label, class_name="w-[120px] whitespace-nowrap", size="2"),
        rx.cond(
            default_value,
            rx.icon(
                "badge-check",
                class_name="w-4 h-4 text-teal-500",
                stroke_width=2,
            ),
            rx.icon(
                "badge-alert",
                class_name="w-4 h-4 text-gray-500",
                stroke_width=2,
            ),
        ),
        class_name="w-full",
    )


def profile_roles(
    is_admin: bool = False, is_active: bool = False, is_verified: bool = False
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("boxes", class_name="w-4 h-4", stroke_width=1.5),
            rx.text("Status"),
            class_name="w-full items-center gap-2",
        ),
        profile_state("Administrator", is_admin),
        profile_state("Aktiv", is_active),
        profile_state("Verifiziert", is_verified),
        class_name="flex-col w-full",
    )
