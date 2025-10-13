import reflex as rx


def delete_dialog(
    title: str,
    content: str,
    on_click: rx.EventHandler,
    icon_button: bool = False,
    class_name: str = "dialog",
    **kwargs,
) -> rx.Component:
    """Generic delete confirmation dialog.

    Args:
        title: Dialog title
        content: The name/identifier of the item to delete
        on_click: Event handler for delete action
        icon_button: If True, use icon_button instead of button for trigger
        **kwargs: Additional props for the trigger button
    """
    # Create the appropriate trigger based on icon_button parameter
    if icon_button:
        trigger = rx.icon_button(rx.icon("trash-2", size=19), **kwargs)
    else:
        trigger = rx.button(rx.icon("trash-2", size=16), **kwargs)

    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(trigger),
        rx.alert_dialog.content(
            rx.alert_dialog.title(title),
            rx.alert_dialog.description(
                rx.text(
                    "Bist du sicher, dass du ",
                    rx.text.strong(content),
                    " löschen möchtest? ",
                    "Diese Aktion wird das ausgewählte Element und alle zugehörigen ",
                    "Daten dauerhaft löschen. Dieser Vorgang kann nicht rückgängig ",
                    "gemacht werden!",
                ),
                class_name="mb-4",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Abbrechen",
                        class_name=(
                            "bg-gray-100 text-gray-700 hover:bg-gray-200 "
                            "px-4 py-2 rounded"
                        ),
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Löschen",
                        class_name=(
                            "bg-red-500 text-white hover:bg-red-600 px-4 py-2 rounded"
                        ),
                        on_click=on_click,
                    )
                ),
                class_name="justify-end gap-3",
            ),
            class_name=class_name,
        ),
    )


def dialog_header(icon: str, title: str, description: str) -> rx.Component:
    """Reusable dialog header component."""
    return rx.hstack(
        rx.badge(
            rx.icon(tag=icon, size=34),
            class_name="bg-green-500 text-white rounded-full p-3",
        ),
        rx.vstack(
            rx.dialog.title(
                title,
                class_name="font-bold m-0",
            ),
            rx.dialog.description(description),
            class_name="space-y-1 h-full items-start",
        ),
        class_name="h-full space-x-4 mb-6 items-center w-full",
    )


def dialog_buttons(submit_text: str, spacing: str = "3") -> rx.Component:
    """Reusable dialog action buttons."""
    return rx.flex(
        rx.dialog.close(
            rx.button(
                "Abbrechen",
                class_name=(
                    "bg-gray-100 text-gray-700 hover:bg-gray-200 px-4 py-2 rounded"
                ),
            ),
        ),
        rx.form.submit(
            rx.dialog.close(
                rx.button(submit_text, class_name="px-4 py-2 rounded"),
            ),
            as_child=True,
        ),
        class_name=f"pt-8 gap-{spacing} mt-4 justify-end",
    )
