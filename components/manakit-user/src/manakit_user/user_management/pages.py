from collections.abc import Callable

import reflex as rx

from manakit_ui.components.header import header
from manakit_user.authentication.components import (
    login_form,
)
from manakit_user.authentication.states import LOGIN_ROUTE, UserSession
from manakit_user.authentication.templates import (
    authenticated,
    default_layout,
)
from manakit_user.user_management.components.user_profile import profile_roles
from manakit_user.user_management.states.profile_states import (
    MIN_PASSWORD_LENGTH,
    ProfileState,
)

ROLES = []


@default_layout(route=LOGIN_ROUTE, title="Login")
def login_page() -> rx.Component:
    return login_form(logo="/img/logo.svg", logo_dark="/img/logo_dark.svg")


def create_profile_page(
    navbar: rx.Component,
    route: str = "/profile",
    title: str = "Profil",
) -> Callable:
    """Create the profile page with authentication.

    Args:
        navbar: The navigation bar to use in the page.

    Returns:
        The profile page component.
    """

    @authenticated(
        route=route,
        title=title,
        navbar=navbar,
    )
    def _profile_page() -> rx.Component:
        """The profile page.

        Returns:
            The UI for the profile page.
        """
        return rx.vstack(
            header("Profil"),
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.icon("square-user-round", class_name="w-4 h-4"),
                        rx.heading("Persönliche Informationen", size="5"),
                        class_name="items-center",
                    ),
                    rx.text("Aktualisiere deine persönlichen Informationen.", size="3"),
                    class_name="w-full",
                ),
                rx.form.root(
                    rx.vstack(
                        rx.vstack(
                            rx.cond(
                                UserSession.user.avatar_url,
                                rx.avatar(
                                    src=UserSession.user.avatar_url,
                                    class_name="w-14 h-14 mb-[6px]",
                                ),
                            ),
                            rx.hstack(
                                rx.icon("user", class_name="w-4 h-4", stroke_width=1.5),
                                rx.text("Name"),
                                class_name="w-full items-center gap-2",
                            ),
                            rx.input(
                                placeholder="dein Name",
                                type="text",
                                class_name="w-full",
                                name="lastname",
                                default_value=rx.cond(
                                    UserSession.user.name, UserSession.user.name, ""
                                ),
                                disabled=True,
                            ),
                            class_name="flex-col gap-1 w-full",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.icon(
                                    "at-sign", class_name="w-4 h-4", stroke_width=1.5
                                ),
                                rx.text("E-Mail / Benutzername"),
                                class_name="w-full items-center gap-2",
                            ),
                            rx.input(
                                placeholder="deine E-Mail-Adresse",
                                type="email",
                                default_value=UserSession.user.email,
                                class_name="w-full",
                                name="mail",
                                disabled=True,
                            ),
                            class_name="flex-col gap-1 w-full",
                        ),
                        rx.cond(
                            UserSession.user,
                            profile_roles(
                                is_admin=UserSession.user.is_admin,
                                is_active=UserSession.user.is_active,
                                is_verified=UserSession.user.is_verified,
                            ),
                            profile_roles(
                                is_admin=False,
                                is_active=False,
                                is_verified=False,
                            ),
                        ),
                        class_name="w-full gap-5",
                    ),
                    class_name="w-full max-w-[325px]",
                ),
                class_name="w-full gap-4 flex-col md:flex-row",
            ),
            rx.divider(),
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.icon("key-round", class_name="w-4 h-4"),
                        rx.heading("Passwort ändern", size="5"),
                        class_name="items-center",
                    ),
                    rx.text(
                        "Aktualisiere dein Passwort. Ein neues Passwort muss der ",
                        "Passwort-Richtlinie entsprechen:",
                        size="3",
                    ),
                    rx.list.unordered(
                        rx.list.item(f"Mindestens {MIN_PASSWORD_LENGTH} Zeichen"),
                        rx.list.item("Mindestens ein Großbuchstabe"),
                        rx.list.item("Mindestens ein Kleinbuchstabe"),
                        rx.list.item("Mindestens eine Zahl"),
                        rx.list.item("Mindestens ein Sonderzeichen"),
                        size="2",
                    ),
                    class_name="w-full",
                ),
                rx.form.root(
                    rx.vstack(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("lock", class_name="w-4 h-4", stroke_width=1.5),
                                rx.text("Aktuelles Passwort"),
                                class_name="w-full items-center gap-2",
                            ),
                            rx.input(
                                placeholder="dein aktuelles Passwort",
                                type="password",
                                default_value="",
                                class_name="w-full",
                                name="current_password",
                                value=ProfileState.current_password,
                                on_change=ProfileState.set_current_password,
                            ),
                            class_name="flex-col gap-1 w-full",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.icon(
                                    "lock-keyhole-open",
                                    class_name="w-4 h-4",
                                    stroke_width=1.5,
                                ),
                                rx.text("Neues Passwort"),
                                class_name="w-full items-center gap-2",
                            ),
                            rx.hstack(
                                rx.input(
                                    placeholder="dein neues Passwort",
                                    type="password",
                                    default_value="",
                                    class_name="w-full",
                                    name="new_password",
                                    value=ProfileState.new_password,
                                    on_change=ProfileState.set_new_password,
                                ),
                                class_name="gap-2 w-full",
                            ),
                            class_name="flex-col gap-1 w-full",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.icon(
                                    "lock-keyhole",
                                    class_name="w-4 h-4",
                                    stroke_width=1.5,
                                ),
                                rx.text("Passwort bestätigen"),
                                class_name="w-full items-center gap-2",
                            ),
                            rx.input(
                                placeholder="bestätige dein neues Passwort",
                                type="password",
                                default_value="",
                                class_name="w-full",
                                name="confirm_password",
                                value=ProfileState.confirm_password,
                                on_change=ProfileState.set_confirm_password,
                            ),
                            class_name="flex-col gap-1 w-full",
                        ),
                        rx.button(
                            "Passwort aktualisieren", type="submit", class_name="w-full"
                        ),
                        class_name="w-full gap-5",
                    ),
                    class_name="w-full max-w-[325px]",
                    on_submit=ProfileState.handle_password_update,
                    reset_on_submit=True,
                ),
                class_name="w-full gap-4 flex-col md:flex-row",
            ),
            class_name="w-full gap-6 max-w-[800px]",
        )

    return _profile_page
