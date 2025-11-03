import reflex as rx

from appkit_user.authentication.components import oauth_login_splash
from appkit_user.authentication.states import LoginState
from appkit_user.configuration import OAuthProvider


def page(provider: OAuthProvider) -> rx.Component:
    return rx.theme(
        rx.center(
            oauth_login_splash(provider),
            class_name="splash-container",
        ),
        has_background=True,
    )


@rx.page(
    route="/oauth/github/callback",
    title="Anmeldung mit Github",
    on_load=LoginState.handle_oauth_callback(OAuthProvider.GITHUB),
)
def github_oauth_callback_page() -> rx.Component:
    return page(OAuthProvider.GITHUB)


@rx.page(
    route="/oauth/azure/callback",
    title="Anmeldung mit Azure",
    on_load=LoginState.handle_oauth_callback(OAuthProvider.AZURE),
)
def azure_oauth_callback_page() -> rx.Component:
    return page(OAuthProvider.AZURE)
