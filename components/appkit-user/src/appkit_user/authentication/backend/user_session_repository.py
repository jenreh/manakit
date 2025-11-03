from datetime import datetime
from enum import StrEnum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from appkit_user.authentication.backend.entities import (
    UserSessionEntity,
)


class DefaultUserRoles(StrEnum):
    """Default user roles."""

    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"


async def get_user_session(
    db: AsyncSession, user_id: int, session_id: str
) -> UserSessionEntity | None:  # Return type can be None if not found
    """Get a user session."""
    stmt = select(UserSessionEntity).where(
        UserSessionEntity.user_id == user_id,
        UserSessionEntity.session_id == session_id,
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_or_update_user_session(
    db: AsyncSession, user_id: int, session_id: str, expires_at: datetime
) -> UserSessionEntity:
    """Create or update a user session."""
    # First, try to get the existing session
    get_stmt = select(UserSessionEntity).where(
        UserSessionEntity.user_id == user_id,
        UserSessionEntity.session_id == session_id,
    )
    result = await db.execute(get_stmt)
    session = result.scalars().first()

    if not session:
        session = UserSessionEntity(
            user_id=user_id, session_id=session_id, expires_at=expires_at
        )
        db.add(session)
    else:
        session.expires_at = expires_at

    await db.commit()
    await db.refresh(session)
    return session


async def delete_user_session(db: AsyncSession, user_id: int, session_id: str) -> None:
    """Delete a user session."""
    get_stmt = select(UserSessionEntity).where(
        UserSessionEntity.user_id == user_id,
        UserSessionEntity.session_id == session_id,
    )
    result = await db.execute(get_stmt)
    session = result.scalars().first()

    if session:
        await db.delete(session)
        await db.commit()
