# ruff: noqa: ARG002, SLF001, S105, S106
"""Tests for UserSession lifecycle.

Covers session creation, lookup, the DB retry helper, termination and
prolongation.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from _auth_state_stubs import (
    _PATCH,
    _StubLoginState,
    _StubUserSession,
    _user_entity,
)

# ============================================================================
# UserSession tests
# ============================================================================


class TestSessionCreation:
    @pytest.mark.asyncio
    async def test_create_session_sets_token_and_user(self) -> None:
        state = _StubUserSession()
        entity = _user_entity(42, "alice")

        mock_session = AsyncMock()
        with patch(f"{_PATCH}.session_repo") as mock_repo:
            mock_repo.save = AsyncMock()
            await state._create_session(mock_session, entity)

        assert state.auth_token != ""
        assert len(state.auth_token) == 64
        assert state.user_id == 42
        assert state.user is not None
        assert state.user.name == "alice"

    @pytest.mark.asyncio
    async def test_create_session_mirrors_token_into_cookie(self) -> None:
        """The cookie must carry the same token local storage holds.

        Plain HTTP transports (page loads, REST/MCP) cannot read local storage,
        so the cookie is the only credential they see. If it drifts from
        ``auth_token`` the HTTP guard rejects an otherwise valid session.
        """
        state = _StubUserSession()

        with patch(f"{_PATCH}.session_repo") as mock_repo:
            mock_repo.save = AsyncMock()
            await state._create_session(AsyncMock(), _user_entity(42, "alice"))

        assert state.session_cookie == state.auth_token
        assert state.session_cookie != ""

    @pytest.mark.asyncio
    async def test_create_session_primes_aware_utc_expiry_cache(self) -> None:
        """The expiry cache is primed so the guards can skip the DB round trip."""
        state = _StubUserSession()
        before = datetime.now(UTC)

        with patch(f"{_PATCH}.session_repo") as mock_repo:
            mock_repo.save = AsyncMock()
            await state._create_session(AsyncMock(), _user_entity(42, "alice"))

        assert state._session_expires_at is not None
        # Aware UTC in state; the naive-UTC compensation applies to the DB only.
        assert state._session_expires_at.tzinfo is not None
        assert state._session_expires_at > before
        assert state._has_unexpired_cache() is True

        # The row itself keeps the naive-UTC value the TIMESTAMP column expects.
        stored_expiry = mock_repo.save.await_args.args[3]
        assert stored_expiry.tzinfo is None


class TestFindValidSession:
    @pytest.mark.asyncio
    async def test_by_user_and_token(self) -> None:
        state = _StubUserSession()
        state.user_id = 1
        state.auth_token = "token-abc"

        mock_db = AsyncMock()
        with patch(f"{_PATCH}.session_repo") as mock_repo:
            mock_repo.find_by_user_and_session_id = AsyncMock(
                return_value="session-obj"
            )
            result = await state._find_valid_session(mock_db)

        assert result == "session-obj"

    @pytest.mark.asyncio
    async def test_fallback_to_token_only(self) -> None:
        state = _StubUserSession()
        state.user_id = 0
        state.auth_token = "token-abc"

        mock_db = AsyncMock()
        with patch(f"{_PATCH}.session_repo") as mock_repo:
            mock_repo.find_by_session_id = AsyncMock(return_value="session-obj")
            result = await state._find_valid_session(mock_db)

        assert result == "session-obj"

    @pytest.mark.asyncio
    async def test_no_credentials(self) -> None:
        state = _StubUserSession()
        state.user_id = 0
        state.auth_token = ""

        mock_db = AsyncMock()
        result = await state._find_valid_session(mock_db)
        assert result is None


class TestExecuteDbOperation:
    @pytest.mark.asyncio
    async def test_success(self) -> None:
        state = _StubUserSession()

        with patch(f"{_PATCH}.get_asyncdb_session") as mock_session:
            session = AsyncMock()
            mock_session.return_value.__aenter__ = AsyncMock(return_value=session)
            mock_session.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await state._execute_db_operation(AsyncMock(return_value="ok"))

        assert result == "ok"

    @pytest.mark.asyncio
    async def test_retries_on_error(self) -> None:
        state = _StubUserSession()
        state.user_id = 1

        call_count = 0

        async def flaky_op(_db):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("SSL closed")
            return "recovered"

        with (
            patch(f"{_PATCH}.get_asyncdb_session") as mock_session,
            patch(f"{_PATCH}.asyncio.sleep", new_callable=AsyncMock),
        ):
            session = AsyncMock()
            mock_session.return_value.__aenter__ = AsyncMock(return_value=session)
            mock_session.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await state._execute_db_operation(flaky_op)

        assert result == "recovered"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_raises_after_all_retries(self) -> None:
        state = _StubUserSession()
        state.user_id = 1

        with (
            patch(f"{_PATCH}.get_asyncdb_session") as mock_session,
            patch(f"{_PATCH}.asyncio.sleep", new_callable=AsyncMock),
        ):
            session = AsyncMock()
            mock_session.return_value.__aenter__ = AsyncMock(return_value=session)
            mock_session.return_value.__aexit__ = AsyncMock(return_value=False)

            with pytest.raises(RuntimeError, match="permanent"):
                await state._execute_db_operation(
                    AsyncMock(side_effect=RuntimeError("permanent"))
                )


class TestTerminateSession:
    @pytest.mark.asyncio
    async def test_success(self) -> None:
        state = _StubUserSession()
        state.auth_token = "token"
        state.user_id = 1

        with (
            patch(f"{_PATCH}.get_asyncdb_session") as mock_session,
            patch(f"{_PATCH}.session_repo") as mock_repo,
        ):
            session = AsyncMock()
            mock_session.return_value.__aenter__ = AsyncMock(return_value=session)
            mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
            mock_repo.delete_by_user_and_session_id = AsyncMock()

            await state.terminate_session()

        assert state.auth_token == ""
        assert state.user_id == 0

    @pytest.mark.asyncio
    async def test_error_still_resets(self) -> None:
        state = _StubUserSession()
        state.auth_token = "token"
        state.user_id = 1

        with (
            patch(f"{_PATCH}.get_asyncdb_session") as mock_session,
            patch(f"{_PATCH}.asyncio.sleep", new_callable=AsyncMock),
            patch(f"{_PATCH}.session_repo") as mock_repo,
        ):
            session = AsyncMock()
            mock_session.return_value.__aenter__ = AsyncMock(return_value=session)
            mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
            mock_repo.delete_by_user_and_session_id = AsyncMock(
                side_effect=RuntimeError("fail")
            )

            await state.terminate_session()

        # State should still be reset
        assert state.auth_token == ""
        assert state.user_id == 0

    @pytest.mark.asyncio
    async def test_clears_inherited_vars_when_called_on_login_state(self) -> None:
        """The cookie and the expiry cache must be cleared *explicitly*.

        ``terminate_session`` is also invoked on ``LoginState``, where
        ``session_cookie`` and ``_session_expires_at`` are vars inherited from
        ``UserSession`` — and ``reset()`` walks only the substate's own vars.
        Without the explicit assignments a logout would leave a live cookie and
        a still-unexpired cache behind, which the session filter would then
        happily wave through.
        """
        state = _StubLoginState()
        state.auth_token = "token"
        state.session_cookie = "token"
        state.user_id = 1
        state._session_expires_at = datetime.now(UTC) + timedelta(minutes=25)

        with (
            patch(f"{_PATCH}.get_asyncdb_session") as mock_session,
            patch(f"{_PATCH}.session_repo") as mock_repo,
        ):
            session = AsyncMock()
            mock_session.return_value.__aenter__ = AsyncMock(return_value=session)
            mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
            mock_repo.delete_by_user_and_session_id = AsyncMock()

            await state.terminate_session()

        assert state.session_cookie == ""
        assert state._session_expires_at is None
        assert state._has_unexpired_cache() is False


class TestProlongSession:
    @pytest.mark.asyncio
    async def test_skip_when_not_authenticated(self) -> None:
        state = _StubUserSession()
        state.user_id = 0
        state.auth_token = ""

        # Should return early without DB call
        await state.prolong_session()

    @pytest.mark.asyncio
    async def test_prolongs_valid_session(self) -> None:
        """Prolonging pushes both the DB row and the cached expiry forward.

        The cache is what the guards consult before hitting the database, so a
        prolonged session that forgets to move it would still be logged out at
        the *old* expiry instant.
        """
        state = _StubUserSession()
        state.user_id = 1
        state.auth_token = "token"
        previous_expiry = datetime.now(UTC) + timedelta(minutes=1)
        state._session_expires_at = previous_expiry

        mock_user_session = MagicMock()
        mock_user_session.is_expired.return_value = False

        with (
            patch(f"{_PATCH}.get_asyncdb_session") as mock_session_ctx,
            patch(f"{_PATCH}.session_repo") as mock_repo,
        ):
            session = AsyncMock()
            mock_session_ctx.return_value.__aenter__ = AsyncMock(return_value=session)
            mock_session_ctx.return_value.__aexit__ = AsyncMock(return_value=False)
            mock_repo.find_by_user_and_session_id = AsyncMock(
                return_value=mock_user_session
            )

            await state.prolong_session()

        assert state._session_expires_at is not None
        assert state._session_expires_at > previous_expiry
        assert state._session_expires_at.tzinfo is not None
        # The row keeps naive UTC for the TIMESTAMP column.
        assert mock_user_session.expires_at.tzinfo is None
        session.commit.assert_awaited()

    @pytest.mark.asyncio
    async def test_expired_session_is_not_prolonged(self) -> None:
        state = _StubUserSession()
        state.user_id = 1
        state.auth_token = "token"
        state._session_expires_at = None

        mock_user_session = MagicMock()
        mock_user_session.is_expired.return_value = True

        with (
            patch(f"{_PATCH}.get_asyncdb_session") as mock_session_ctx,
            patch(f"{_PATCH}.session_repo") as mock_repo,
        ):
            session = AsyncMock()
            mock_session_ctx.return_value.__aenter__ = AsyncMock(return_value=session)
            mock_session_ctx.return_value.__aexit__ = AsyncMock(return_value=False)
            mock_repo.find_by_user_and_session_id = AsyncMock(
                return_value=mock_user_session
            )

            await state.prolong_session()

        assert state._session_expires_at is None
        session.commit.assert_not_awaited()
