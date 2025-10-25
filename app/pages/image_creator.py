import reflex as rx

from manakit_imagecreator.pages import image_generator_page
from manakit_user.authentication.components.components import requires_role
from manakit_user.authentication.templates import authenticated

from app.components.navbar import app_navbar
from app.roles import IMAGE_CREATOR_ROLE


@authenticated(
    route="/image-generator",
    title="Assistant",
    description="A demo page for the Assistant UI.",
    navbar=app_navbar(),
    with_header=True,
)
def image_creator_page() -> rx.Component:
    return requires_role(
        image_generator_page(),
        role=IMAGE_CREATOR_ROLE,
        fallback=rx.text(
            "Zugriff verweigert. Sie haben keine Berechtigung, um Bilder zu generieren.",
            padding="64px",
            justify_content="center",
            width="100%",
        ),
    )
