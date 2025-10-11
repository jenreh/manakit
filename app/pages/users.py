import reflex as rx
from knai_anonymizer.pages import ANONYMIZER_ROLE
from knai_avvia import AVVIA_ROLES
from knai_avvia.components.user_rights import user_rights
from knai_hours import TEAM_MANAGER_ROLE
from knai_nmxdia import NMXDIA_ROLES

from manakit_assistant import ASSISTANT_ROLE
from manakit_imagecreator.pages import IMAGE_GENERATOR_ROLE
from manakit_ui.authentication.components import requires_admin
from manakit_ui.authentication.templates import authenticated
from manakit_ui.components.header import header
from manakit_ui.user_management.components.user import users_table

from app.components.navbar import app_navbar

ROLES = [
    ASSISTANT_ROLE,
    ANONYMIZER_ROLE,
    IMAGE_GENERATOR_ROLE,
    TEAM_MANAGER_ROLE,
    *AVVIA_ROLES,
    *NMXDIA_ROLES,
]


@authenticated(
    route="/admin/users",
    title="Users",
    navbar=app_navbar(),
    admin_only=True,
)
def users_page() -> rx.Component:
    additional_components = [
        user_rights,
    ]

    return requires_admin(
        rx.vstack(
            header("Benutzer"),
            users_table(ROLES, additional_components=additional_components),
            width="100%",
            max_width="1200px",
            spacing="6",
        ),
    )
