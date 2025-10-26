import reflex as rx

from manakit_ui.components.header import header
from manakit_user.authentication.components.components import requires_admin
from manakit_user.authentication.templates import authenticated
from manakit_user.user_management.components.user import users_table
from manakit_user.user_management.states.user_states import UserState

from app.components.navbar import app_navbar
from app.roles import ALL_ROLES


@authenticated(
    route="/admin/users",
    title="Users",
    navbar=app_navbar(),
    admin_only=True,
    on_load=[UserState.set_available_roles(ALL_ROLES)],
)
def users_page() -> rx.Component:
    additional_components = []

    return requires_admin(
        rx.vstack(
            header("Benutzer"),
            users_table(additional_components=additional_components),
            width="100%",
            max_width="1200px",
            spacing="6",
        ),
    )
