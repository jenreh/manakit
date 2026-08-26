"""Public API of the appkit-user authentication package.

A consuming app wires the whole session guard with a single import::

    from appkit_user.authentication import add_session_guard, install_session_filter

    app = rx.App(api_transformer=[api_app, add_session_guard])
    install_session_filter(app)

Symbols are resolved lazily (:pep:`562`) on first attribute access. The
submodules of this package are imported directly from several hundred call
sites; eager re-exports would drag the Reflex middleware stack, FastAPI and the
full state tree into every one of them and force configuration resolution at
import time. ``from appkit_user.authentication import X`` still works exactly
as if the imports were eager.
"""

import importlib
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from appkit_user.authentication.http_guard import (
        RequiredSession,
        SessionGuardMiddleware,
        add_session_guard,
        require_session,
    )
    from appkit_user.authentication.session_filter import (
        SessionFilter,
        install_session_filter,
    )
    from appkit_user.authentication.session_validation import (
        LOGIN_ROUTE,
        SessionStatus,
        SessionValidationResult,
        SessionValidator,
        is_public_route,
    )
    from appkit_user.authentication.states import LoginState, UserSession

# Exported name -> submodule that defines it.
_EXPORTS: Final[dict[str, str]] = {
    "LOGIN_ROUTE": "session_validation",
    "LoginState": "states",
    "RequiredSession": "http_guard",
    "SessionFilter": "session_filter",
    "SessionGuardMiddleware": "http_guard",
    "SessionStatus": "session_validation",
    "SessionValidationResult": "session_validation",
    "SessionValidator": "session_validation",
    "UserSession": "states",
    "add_session_guard": "http_guard",
    "install_session_filter": "session_filter",
    "is_public_route": "session_validation",
    "require_session": "http_guard",
}

__all__ = [
    "LOGIN_ROUTE",
    "LoginState",
    "RequiredSession",
    "SessionFilter",
    "SessionGuardMiddleware",
    "SessionStatus",
    "SessionValidationResult",
    "SessionValidator",
    "UserSession",
    "add_session_guard",
    "install_session_filter",
    "is_public_route",
    "require_session",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Import and cache a re-exported symbol on first access."""
    submodule = _EXPORTS.get(name)
    if submodule is None:
        message = f"module {__name__!r} has no attribute {name!r}"
        raise AttributeError(message)
    value = getattr(importlib.import_module(f"{__name__}.{submodule}"), name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """List the lazily exported names alongside the module globals."""
    return sorted(set(__all__) | set(globals()))
