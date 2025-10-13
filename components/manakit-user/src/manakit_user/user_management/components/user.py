import reflex as rx

import manakit_mantine as mn
from manakit_ui.components.dialogs import (
    delete_dialog,
    dialog_buttons,
    dialog_header,
)
from manakit_ui.components.form_inputs import form_field, hidden_field
from manakit_user.authentication.backend.models import User
from manakit_user.user_management.states.user_states import Role, UserState


def user_form_fields(
    user: User | None = None,
    roles: list[Role] | None = None,
) -> rx.Component:
    """Reusable form fields for user add/update dialogs."""
    if roles is None:
        roles = []
    is_edit_mode = user is not None

    # Basic user fields
    basic_fields = [
        hidden_field(
            name="user_id",
            default_value=user.user_id.to_string() if is_edit_mode else "",
        ),
        form_field(
            name="name",
            icon="user",
            label="Name",
            type="text",
            default_value=user.name if is_edit_mode else None,
            required=True,
        ),
        form_field(
            name="email",
            icon="mail",
            label="Email",
            hint="Die E-Mail-Adresse des Benutzers, wird für die Anmeldung verwendet.",
            type="email",
            default_value=user.email if is_edit_mode else None,
            required=True,
            pattern=r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$",
        ),
        form_field(
            name="password",
            icon="lock",
            label="Initiales Passwort" if not is_edit_mode else "Passwort",
            type="password",
            hint="Leer lassen, um das aktuelle Passwort beizubehalten",
            required=False,
        ),
    ]

    # Status switches (only for edit mode)
    status_fields = []
    if is_edit_mode:
        status_fields = [
            rx.hstack(
                rx.switch(
                    name="is_active",
                    default_checked=(
                        user.is_active if user.is_active is not None else False
                    ),
                ),
                rx.text("Aktiv", size="2"),
            ),
            rx.hstack(
                rx.switch(
                    name="is_verified",
                    default_checked=(
                        user.is_verified if user.is_verified is not None else False
                    ),
                ),
                rx.text("Verifiziert", size="2"),
            ),
            rx.hstack(
                rx.switch(
                    name="is_admin",
                    default_checked=(
                        user.is_admin if user.is_admin is not None else False
                    ),
                ),
                rx.text("Superuser", size="2"),
            ),
        ]

    # Role fields (available for both add and edit modes)
    if roles:
        role_fields = [
            rx.text("Berechtigungen", size="3", weight="bold"),
            rx.flex(
                rx.foreach(
                    roles,
                    lambda role: rx.box(
                        rx.checkbox(
                            role.label,
                            name=f"role_{role.name.lower()}",
                            default_checked=(
                                user.roles.contains(role.name)
                                if is_edit_mode and user.roles is not None
                                else False
                            ),
                        ),
                        class_name="w-[30%] max-w-[30%] flex-grow",
                    ),
                ),
                class_name="w-full flex-wrap gap-3",
            ),
        ]

    # Combine all fields
    all_fields = basic_fields + status_fields + role_fields

    return rx.flex(
        *all_fields,
        class_name=rx.cond(is_edit_mode, "flex-col gap-0", "flex-col gap-3"),
    )


def add_user_button(
    label: str = "Benutzer hinzufügen",
    icon: str = "plus",
    icon_size: int = 19,
    roles: list[Role] | None = None,
    **kwargs,
) -> rx.Component:
    if roles is None:
        roles = []

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon(icon, size=icon_size),
                rx.text(label, display=["none", "none", "block"]),
                **kwargs,
            ),
        ),
        rx.dialog.content(
            dialog_header(
                icon="users",
                title="Benutzer hinzufügen",
                description="Bitte füllen Sie das Formular mit den Benutzerdaten aus.",
            ),
            rx.flex(
                rx.form.root(
                    user_form_fields(roles=roles),
                    dialog_buttons(
                        submit_text="Benutzer speichern",
                    ),
                    on_submit=UserState.create_user,
                    reset_on_submit=False,
                ),
                class_name="w-full flex-col gap-4",
            ),
            class_name="dialog",
        ),
    )


def update_user_button(
    user: User,
    roles: list[Role],
    icon: str = "square-pen",
    icon_size: int = 19,
    **kwargs,
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.icon_button(
                rx.icon(icon, size=icon_size),
                on_click=lambda: UserState.select_user(user.user_id),
                **kwargs,
            ),
        ),
        rx.dialog.content(
            dialog_header(
                icon="users",
                title="Benutzer bearbeiten",
                description="Aktualisieren Sie die Benutzerdaten",
            ),
            rx.flex(
                rx.form.root(
                    user_form_fields(user=user, roles=roles),
                    dialog_buttons(
                        submit_text="Benutzer aktualisieren",
                    ),
                    on_submit=UserState.update_user,
                    reset_on_submit=False,
                ),
                class_name="w-full flex-col gap-4",
            ),
            class_name="dialog",
        ),
    )


def delete_user_button(user: User, **kwargs) -> rx.Component:
    """Use the generic delete dialog component."""
    return delete_dialog(
        title="Löschen bestätigen",
        content=rx.cond(user.email, user.email, "Unbekannter Benutzer"),
        on_click=lambda: UserState.delete_user(user.user_id),
        icon_button=True,
        **kwargs,
    )


def users_table_row(
    user: User, roles: list[Role], additional_components: list | None = None
) -> rx.Component:
    """Show a customer in a table row.

    Args:
        user: The user object to display
        roles: List of available roles
        additional_components: Optional list of component functions that will be
                              called with (user=user, roles=roles) and rendered
                              to the left of the edit button
    """
    if additional_components is None:
        additional_components = []

    # Generate additional components with the same parameters as edit/delete buttons
    rendered_additional_components = [
        component_func(user=user, roles=roles)
        for component_func in additional_components
    ]

    return mn.table.tr(
        mn.table.td(
            rx.cond(user.name, user.name, ""),
            class_name="whitespace-nowrap",
        ),
        mn.table.td(
            rx.cond(user.email, user.email, ""),
            class_name="whitespace-nowrap",
        ),
        mn.table.td(
            rx.cond(
                user.is_active,
                rx.icon("user-check", color="green", size=21),
                rx.icon("user-x", color="crimson", size=21),
            ),
            class_name="text-center",
        ),
        mn.table.td(
            rx.cond(
                user.is_verified,
                rx.icon("user-check", color="green", size=21),
                rx.icon("user-x", color="crimson", size=21),
            ),
            class_name="text-center",
        ),
        mn.table.td(
            rx.cond(
                user.is_admin,
                rx.icon("user-check", color="green", size=21),
                rx.icon("user-x", color="crimson", size=21),
            ),
            class_name="text-center",
        ),
        mn.table.td(
            rx.hstack(
                *rendered_additional_components,
                update_user_button(user=user, roles=roles, variant="surface"),
                delete_user_button(
                    user=user, variant="surface", color_scheme="crimson"
                ),
                class_name="whitespace-nowrap",
            ),
        ),
        class_name="justify-center items-center",
        # style={"_hover": {"bg": rx.color("gray", 2)}},
    )


def loading() -> rx.Component:
    """Loading indicator for the users table."""
    return mn.table.row(
        mn.table.td(
            rx.hstack(
                rx.spinner(size="3"),
                rx.text("Lade Benutzer...", size="3"),
            ),
            col_span=6,
            class_name="text-center justify-center",
        ),
    )


def users_table(
    roles: list[Role], additional_components: list | None = None
) -> rx.Component:
    """Create a users table with optional additional components.

    Args:
        roles: List of available roles for user management
        additional_components: Optional list of component functions that will be
                              rendered to the left of the edit button for each user.
                              Each function will be called with (user=user, roles=roles)
    """
    return rx.fragment(
        rx.flex(
            add_user_button(roles=roles),
            rx.spacer(),
        ),
        mn.table(
            mn.table.thead(
                mn.table.tr(
                    mn.table.th("Name"),
                    mn.table.th("Email", width="auto"),
                    mn.table.th("Aktiv", width="90px"),
                    mn.table.th("Verifiziert", width="90px"),
                    mn.table.th("Admin", width="90px"),
                    mn.table.th("", width="110px"),
                ),
            ),
            rx.cond(
                UserState.is_loading,
                mn.table.tbody(loading()),
                mn.table.tbody(
                    rx.foreach(
                        UserState.users,
                        lambda user: users_table_row(
                            user=user,
                            roles=roles,
                            additional_components=additional_components,
                        ),
                    )
                ),
            ),
            highlight_on_hover=True,
            sticky_header=True,
            class_name="w-full",
            on_mount=UserState.load_users,
        ),
    )
