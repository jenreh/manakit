from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from appkit_user.authentication.backend.entities import (
    OAuthStateEntity,
)


async def cleanup_expired_oauth_states(db: AsyncSession) -> int:
    """Clean up expired OAuth states and return count of deleted records."""
    now = datetime.now(UTC)
    stmt = delete(OAuthStateEntity).where(OAuthStateEntity.expires_at < now)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount


async def cleanup_oauth_states_for_session(db: AsyncSession, session_id: str) -> int:
    """Clean up OAuth states for a specific session."""
    stmt = delete(OAuthStateEntity).where(OAuthStateEntity.session_id == session_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount


async def get_oauth_state(
    db: AsyncSession, state: str, provider: str
) -> OAuthStateEntity | None:
    stmt = select(OAuthStateEntity).where(
        OAuthStateEntity.state == state,
        OAuthStateEntity.provider == provider,
        OAuthStateEntity.expires_at > datetime.now(UTC),  # Check not expired
    )
    result = await db.execute(stmt)
    oauth_state = result.scalars().first()

    if oauth_state:
        return oauth_state
    return None
