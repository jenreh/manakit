# ruff: noqa: ARG002, SLF001, S105, S106
"""Tests for the transport-agnostic session validation core.

Covers the public-route allowlist and path normalization, every
``SessionValidator.validate`` classification branch, the repository routing
by ``user_id``, and the naive-UTC compensation for the ``auth_sessions``
``expires_at`` column.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from appkit_user.authentication.backend.database import UserSessionEntity
from appkit_user.authentication.session_validation import (
    LOGIN_ROUTE,
    SessionStatus,
    SessionValidationResult,
    SessionValidator,
    _auth_config,
    is_public_route,
    is_session_filter_enabled,
    safe_redirect_path,
    session_cookie_name,
)
from appkit_user.configuration import AuthenticationConfiguration

_PATCH = "appkit_user.authentication.session_validation"

_TOKEN = "tok-abcdef"


# ============================================================================
# Helpers
# ============================================================================


def _config(**overrides: object) -> AuthenticationConfiguration:
    """Build a real configuration object with the shipped defaults."""
    values: dict[str, object] = {
        "server_url": "http://localhost",
        "server_port": 3000,
    }
    values.update(overrides)
    return AuthenticationConfiguration(**values)  # type: ignore[arg-type]


def _user_entity(user_id: int = 7, is_active: bool = True) -> SimpleNamespace:
    """Stand-in for a ``UserEntity`` row that ``User.model_validate`` accepts."""
    return SimpleNamespace(
        id=user_id,
        name="Test User",
        email="test@example.com",
        avatar_url="",
        is_verified=True,
        is_admin=False,
        is_active=is_active,
        needs_password_reset=False,
        roles=["user"],
    )


def _row(
    expires_at: datetime | None = None,
    user: SimpleNamespace | None = None,
    user_id: int = 7,
) -> MagicMock:
    """Build a session row whose ``is_expired`` runs the real entity logic.

    ``expires_at`` defaults to a *naive* future timestamp, matching what the
    ``auth_sessions`` table actually stores.
    """
    row = MagicMock()
    row.id = 42
    row.user_id = user_id
    row.session_id = _TOKEN
    row.expires_at = (
        expires_at
        if expires_at is not None
        else (datetime.now(UTC) + timedelta(minutes=25)).replace(tzinfo=None)
    )
    row.user = _user_entity(user_id=user_id) if user is None else user
    # Bind the production expiry check so the naive->aware compensation is
    # exercised for real rather than stubbed away.
    row.is_expired = lambda: UserSessionEntity.is_expired(row)
    return row


def _db_context(db: AsyncMock) -> AsyncMock:
    """Async context manager yielding ``db``."""
    cm = AsyncMock()
    cm.__aenter__ = AsyncMock(return_value=db)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


@contextmanager
def _patched_db(
    row: MagicMock | None = None,
    error: Exception | None = None,
) -> Iterator[SimpleNamespace]:
    """Patch the DB session factory and the session repository."""
    db = AsyncMock()
    with (
        patch(f"{_PATCH}.get_asyncdb_session", return_value=_db_context(db)) as factory,
        patch(f"{_PATCH}.session_repo") as repo,
    ):
        if error is not None:
            repo.find_by_user_and_session_id = AsyncMock(side_effect=error)
            repo.find_by_session_id = AsyncMock(side_effect=error)
        else:
            repo.find_by_user_and_session_id = AsyncMock(return_value=row)
            repo.find_by_session_id = AsyncMock(return_value=row)
        yield SimpleNamespace(db=db, repo=repo, factory=factory)


@pytest.fixture
def auth_config() -> Iterator[AuthenticationConfiguration]:
    """Replace the lru_cached config lookup with a real config object."""
    config = _config()
    with patch(f"{_PATCH}._auth_config", return_value=config):
        yield config


# ============================================================================
# is_public_route
# ============================================================================


@pytest.mark.usefixtures("auth_config")
@pytest.mark.parametrize(
    "path",
    ["/login", "/password-reset", "/password-reset/confirm"],
)
def test_public_route_exact_match(path: str) -> None:
    assert is_public_route(path) is True


@pytest.mark.usefixtures("auth_config")
@pytest.mark.parametrize("provider", ["github", "azure", "google", "apple"])
def test_public_route_oauth_callback_glob(provider: str) -> None:
    """``/oauth/*/callback`` must cover every configured provider."""
    assert is_public_route(f"/oauth/{provider}/callback") is True


@pytest.mark.usefixtures("auth_config")
@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/profile",
        "/users",
        "/oauth/github",
        "/oauth/github/callback/evil",
        "/login-extra",
        "/password-reset-extra",
    ],
)
def test_public_route_is_default_deny(path: str) -> None:
    assert is_public_route(path) is False


@pytest.mark.usefixtures("auth_config")
@pytest.mark.parametrize(
    "path",
    ["/login/", "/login?next=/profile", "/login#anchor", "/login/?next=/x"],
)
def test_public_route_normalizes_trailing_slash_and_query(path: str) -> None:
    assert is_public_route(path) is True


def test_public_route_preserves_bare_root() -> None:
    """A path that normalizes down to ``/`` stays ``/``, never the empty string."""
    with patch(f"{_PATCH}._auth_config", return_value=_config(public_routes=["/"])):
        assert is_public_route("/") is True
        assert is_public_route("//") is True
        assert is_public_route("/?a=1") is True
        assert is_public_route("/profile") is False


def test_public_route_empty_allowlist_denies_everything() -> None:
    with patch(f"{_PATCH}._auth_config", return_value=_config(public_routes=[])):
        assert is_public_route("/login") is False


def test_public_route_is_case_sensitive(
    auth_config: AuthenticationConfiguration,
) -> None:
    assert is_public_route("/Login") is False


# ============================================================================
# Config accessors and constants
# ============================================================================


def test_session_cookie_name_reads_config() -> None:
    with patch(
        f"{_PATCH}._auth_config", return_value=_config(session_cookie_name="sid")
    ):
        assert session_cookie_name() == "sid"


@pytest.mark.parametrize("enabled", [True, False])
def test_is_session_filter_enabled_reads_config(enabled: bool) -> None:
    with patch(
        f"{_PATCH}._auth_config", return_value=_config(session_filter_enabled=enabled)
    ):
        assert is_session_filter_enabled() is enabled


def test_login_route_constant() -> None:
    assert LOGIN_ROUTE == "/login"


def test_auth_config_resolves_from_registry_once() -> None:
    """The registry lookup is lru_cached; swapping config needs a cache_clear."""
    config = _config()
    registry = MagicMock()
    registry.get.return_value = config
    _auth_config.cache_clear()
    try:
        with patch(f"{_PATCH}.service_registry", return_value=registry):
            assert _auth_config() is config
            assert _auth_config() is config
        registry.get.assert_called_once_with(AuthenticationConfiguration)
    finally:
        _auth_config.cache_clear()


# ============================================================================
# SessionValidationResult
# ============================================================================


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (SessionStatus.VALID, True),
        (SessionStatus.EXPIRED, False),
        (SessionStatus.ABSENT, False),
        (SessionStatus.ERROR, False),
    ],
)
def test_result_is_valid(status: SessionStatus, expected: bool) -> None:
    assert SessionValidationResult(status).is_valid is expected


def test_result_defaults_to_no_user_and_no_expiry() -> None:
    result = SessionValidationResult(SessionStatus.ABSENT)
    assert result.user is None
    assert result.expires_at is None


# ============================================================================
# SessionValidator.validate — no session id
# ============================================================================


@pytest.mark.asyncio
@pytest.mark.parametrize("session_id", ["", "   ", "\t\n"])
async def test_validate_blank_id_is_absent_without_touching_db(
    session_id: str,
) -> None:
    with _patched_db() as env:
        result = await SessionValidator().validate(session_id)

    assert result.status is SessionStatus.ABSENT
    assert result.is_valid is False
    env.factory.assert_not_called()
    env.repo.find_by_session_id.assert_not_awaited()
    env.repo.find_by_user_and_session_id.assert_not_awaited()


# ============================================================================
# SessionValidator.validate — classification
# ============================================================================


@pytest.mark.asyncio
async def test_validate_row_not_found_is_absent() -> None:
    with _patched_db(row=None):
        result = await SessionValidator().validate(_TOKEN)

    assert result.status is SessionStatus.ABSENT
    assert result.user is None


@pytest.mark.asyncio
async def test_validate_expired_row_is_expired() -> None:
    past = (datetime.now(UTC) - timedelta(minutes=1)).replace(tzinfo=None)
    with _patched_db(row=_row(expires_at=past)):
        result = await SessionValidator().validate(_TOKEN)

    assert result.status is SessionStatus.EXPIRED
    assert result.is_valid is False
    assert result.user is None


@pytest.mark.asyncio
async def test_validate_row_without_user_is_expired() -> None:
    row = _row()
    row.user = None
    with _patched_db(row=row):
        result = await SessionValidator().validate(_TOKEN)

    assert result.status is SessionStatus.EXPIRED
    assert result.user is None


@pytest.mark.asyncio
async def test_validate_inactive_user_is_expired() -> None:
    row = _row(user=_user_entity(is_active=False))
    with _patched_db(row=row):
        result = await SessionValidator().validate(_TOKEN)

    assert result.status is SessionStatus.EXPIRED
    assert result.user is None


@pytest.mark.asyncio
async def test_validate_happy_path_returns_user() -> None:
    with _patched_db(row=_row(user=_user_entity(user_id=42))):
        result = await SessionValidator().validate(_TOKEN)

    assert result.status is SessionStatus.VALID
    assert result.is_valid is True
    assert result.user is not None
    assert result.user.user_id == 42
    assert result.user.email == "test@example.com"
    assert result.user.roles == ["user"]


@pytest.mark.asyncio
async def test_validate_returns_aware_utc_expiry_for_naive_column() -> None:
    """Regression guard: ``auth_sessions.expires_at`` is stored naive UTC."""
    naive = (datetime.now(UTC) + timedelta(minutes=25)).replace(tzinfo=None)
    with _patched_db(row=_row(expires_at=naive)):
        result = await SessionValidator().validate(_TOKEN)

    assert result.status is SessionStatus.VALID
    assert result.expires_at is not None
    assert result.expires_at.tzinfo is not None
    assert result.expires_at.utcoffset() == timedelta(0)
    # The wall-clock value must not be shifted, only labelled.
    assert result.expires_at.replace(tzinfo=None) == naive
    # And it must be directly comparable against an aware "now".
    assert result.expires_at > datetime.now(UTC)


@pytest.mark.asyncio
async def test_validate_keeps_already_aware_expiry_unchanged() -> None:
    aware = datetime.now(UTC) + timedelta(minutes=25)
    with _patched_db(row=_row(expires_at=aware)):
        result = await SessionValidator().validate(_TOKEN)

    assert result.expires_at == aware


# ============================================================================
# SessionValidator.validate — repository routing
# ============================================================================


@pytest.mark.asyncio
async def test_validate_scopes_lookup_to_user_when_user_id_known() -> None:
    with _patched_db(row=_row()) as env:
        result = await SessionValidator().validate(_TOKEN, user_id=7)

    assert result.status is SessionStatus.VALID
    env.repo.find_by_user_and_session_id.assert_awaited_once_with(env.db, 7, _TOKEN)
    env.repo.find_by_session_id.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id", [0, -1])
async def test_validate_falls_back_to_token_only_lookup(user_id: int) -> None:
    with _patched_db(row=_row()) as env:
        result = await SessionValidator().validate(_TOKEN, user_id=user_id)

    assert result.status is SessionStatus.VALID
    env.repo.find_by_session_id.assert_awaited_once_with(env.db, _TOKEN)
    env.repo.find_by_user_and_session_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_validate_defaults_to_token_only_lookup() -> None:
    with _patched_db(row=_row()) as env:
        await SessionValidator().validate(_TOKEN)

    env.repo.find_by_session_id.assert_awaited_once_with(env.db, _TOKEN)


# ============================================================================
# SessionValidator.validate — failure handling
# ============================================================================


@pytest.mark.asyncio
async def test_validate_returns_error_when_repository_raises() -> None:
    with _patched_db(error=RuntimeError("connection reset")):
        result = await SessionValidator().validate(_TOKEN, user_id=7)

    assert result.status is SessionStatus.ERROR
    assert result.is_valid is False
    assert result.user is None
    assert result.expires_at is None


@pytest.mark.asyncio
async def test_validate_returns_error_when_session_factory_raises() -> None:
    with patch(
        f"{_PATCH}.get_asyncdb_session", side_effect=OSError("no database configured")
    ):
        result = await SessionValidator().validate(_TOKEN)

    assert result.status is SessionStatus.ERROR


@pytest.mark.asyncio
async def test_validate_returns_error_when_classification_raises() -> None:
    """A corrupt row must fail closed inside the DB block, not propagate."""
    row = _row(expires_at=None)
    row.expires_at = None  # NULL column -> AttributeError in is_expired()
    with _patched_db(row=row):
        result = await SessionValidator().validate(_TOKEN)

    assert result.status is SessionStatus.ERROR
    assert result.user is None


# ============================================================================
# Redirect-target sanitisation
# ============================================================================


class TestSafeRedirectPath:
    """Post-login targets come from the browser, so they are not trusted."""

    @pytest.mark.parametrize("path", ["/profile", "/users/7", "/a/b?c=d", "/"])
    def test_local_paths_pass_through(self, path: str) -> None:
        assert safe_redirect_path(path) == path

    @pytest.mark.parametrize(
        "path",
        [
            # Verified: Reflex resolves asPath "https://evil.com/x" and
            # "//evil.com/pwn" to a path of "//evil.com/pwn" -- a
            # protocol-relative URL that navigates off-site.
            "//evil.com/pwn",
            "///evil.com",
            "/\\evil.com",
            "https://evil.com",
            "evil.com",
            "",
        ],
    )
    def test_off_site_targets_are_rejected(self, path: str) -> None:
        assert safe_redirect_path(path) == ""
