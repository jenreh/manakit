"""Common templates used between pages in the app."""

from __future__ import annotations

from collections.abc import Callable

import reflex as rx

from manakit_ui.global_states import LoadingState
from manakit_user.authentication.states import (
    LOGIN_ROUTE,
    LoginState,
    UserSession,
)

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]


class ThemeState(rx.State):
    """The state for the theme of the app."""

    # accent_color: str = "crimson"
    gray_color: str = "gray"
    radius: str = "large"
    scaling: str = "100%"
    appearance: str = "inherit"


def require_login(page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:
    """Decorator to require authentication before rendering a page.

    If the user is not authenticated, then redirect to the login page.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """

    def protected_page():
        return rx.fragment(
            rx.cond(
                UserSession.is_authenticated,
                page(),
                rx.center(
                    rx.card(
                        rx.image(
                            rx.color_mode_cond(
                                "/img/logo.svg",
                                "/img/logo_dark.svg",
                            ),
                            height="56px",
                            margin_bottom="1em",
                            margin_left="1em",
                        ),
                        rx.vstack(
                            rx.text(
                                (
                                    "Sie müssen angemeldet sein, um auf diese Seite "
                                    "zuzugreifen. Weiterleitung zum "
                                ),
                                rx.link(
                                    "Login",
                                    href=LOGIN_ROUTE,
                                    color="primary",
                                    width="100%",
                                    align="center",
                                ),
                                "...",
                                on_mount=LoginState.redir,
                            ),
                            width="100%",
                            padding="1em",
                        ),
                        variant="classic",
                        margin_top="-4em",
                        min_width="26em",
                        max_width="26em",
                        width="100%",
                    ),
                    width="100%",
                    height="100vh",
                    class_name="splash-container",
                ),
            ),
        )

    protected_page.__name__ = page.__name__
    return protected_page


def theme_wrapper(content: rx.Component) -> rx.Component:
    return rx.theme(
        content,
        has_background=True,
        gray_color=ThemeState.gray_color,
        radius=ThemeState.radius,
        scaling=ThemeState.scaling,
        appearance=ThemeState.appearance,
        class_name=rx.cond(LoadingState.is_loading, "cursor-wait", ""),
    )


def default_layout(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.EventHandler | list[rx.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app.

    Args:
        route: The route to reach the page.
        title: The title of the page.
        description: The description of the page.
        meta: Additionnal meta to add to the page.
        on_load: The event handler(s) called when the page load.
        script_tags: Scripts to attach to the page.

    Returns:
        The template with the page content.
    """

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        all_meta = [*default_meta, *(meta or [])]

        def templated_page():
            return rx.center(
                page_content(),
                width="100%",
                height="100vh",
                class_name="splash-container",
            )

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def theme_wrap():
            return rx.theme(
                templated_page(),
                has_background=True,
                appearance="dark",
            )

        return theme_wrap

    return decorator


def navbar_layout(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    navbar: rx.Component | None = None,
    with_header: bool = False,
    admin_only: bool = False,
    meta: list[dict] | None = None,  # Updated type hint
    script_tags: list[rx.Component] | None = None,
    on_load: rx.EventHandler | list[rx.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app that requires authentication."""
    if on_load is None:
        on_load = [LoadingState.set_is_loading(False)]
    elif isinstance(on_load, list):
        on_load.append(LoadingState.set_is_loading(False))
    elif isinstance(on_load, rx.EventHandler):
        on_load = [on_load, LoadingState.set_is_loading(False)]

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        all_meta = [*default_meta, *(meta or [])]
        is_admin: bool = UserSession.user.is_admin

        def templated_page(
            content: Callable[[], rx.Component],
            navbar_component: rx.Component,
        ) -> rx.Component:
            return rx.hstack(
                navbar_component,
                rx.flex(
                    rx.vstack(
                        content(),
                        width="100%",
                        padding_top="2.5em",
                    ),
                    width="100%",
                    max_width="100%",
                    padding_top="0",
                    padding_x=rx.cond(with_header, "0", ["auto", "auto", "2em"]),
                ),
                width="100%",
                spacing="0",
                position="relative",
            )

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def theme_wrap():
            # Create navbar component if provided
            navbar_component = navbar if navbar else rx.fragment()
            default_page = theme_wrapper(templated_page(page_content, navbar_component))
            no_permission_page = theme_wrapper(
                templated_page(
                    lambda: rx.center(
                        rx.heading(
                            "Sie haben nicht die notwendigen Berechtigungen um auf diese Seite zuzugreifen.",  # noqa
                            size="4",
                        ),
                        width="100%",
                        margin_top="10em",
                    ),
                    navbar_component,
                )
            )

            return rx.cond(
                admin_only,
                rx.cond(
                    is_admin,
                    default_page,
                    no_permission_page,
                ),
                default_page,
            )

        return theme_wrap

    return decorator


def authenticated(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    navbar: rx.Component | None = None,
    with_header: bool = False,
    admin_only: bool = False,
    meta: list[dict] | None = None,  # Updated type hint
    script_tags: list[rx.Component] | None = None,
    on_load: rx.EventHandler | list[rx.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app that requires authentication."""
    if on_load is None:
        on_load = [LoadingState.set_is_loading(False)]
    elif isinstance(on_load, list):
        on_load.append(LoadingState.set_is_loading(False))
    elif isinstance(on_load, rx.EventHandler):
        on_load = [on_load, LoadingState.set_is_loading(False)]

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        all_meta = [*default_meta, *(meta or [])]
        is_admin: bool = UserSession.user.is_admin

        def templated_page(
            content: Callable[[], rx.Component],
            navbar_component: rx.Component,
        ) -> rx.Component:
            return rx.hstack(
                navbar_component,
                rx.flex(
                    rx.vstack(
                        content(),
                        width="100%",
                        padding_top="2.5em",
                    ),
                    width="100%",
                    max_width="100%",
                    padding_top=rx.cond(with_header, "0", ["1em", "1em", "2em"]),
                    padding_x=rx.cond(with_header, "0", ["auto", "auto", "2em"]),
                ),
                width="100%",
                spacing="0",
                position="relative",
            )

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        @require_login
        def theme_wrap():
            # Create navbar component if provided
            navbar_component = navbar if navbar else rx.fragment()
            default_page = theme_wrapper(templated_page(page_content, navbar_component))
            no_permission_page = theme_wrapper(
                templated_page(
                    lambda: rx.center(
                        rx.heading(
                            "Sie haben nicht die notwendigen Berechtigungen um auf diese Seite zuzugreifen.",  # noqa
                            size="4",
                        ),
                        width="100%",
                        margin_top="10em",
                    ),
                    navbar_component,
                )
            )

            return rx.cond(
                admin_only,
                rx.cond(
                    is_admin,
                    default_page,
                    no_permission_page,
                ),
                default_page,
            )

        return theme_wrap

    return decorator
