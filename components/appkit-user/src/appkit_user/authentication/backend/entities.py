import logging
from datetime import UTC, datetime
from typing import Final, Optional

from sqlalchemy import (
    ARRAY,  # Added import
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Unicode,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine

from appkit_commons.database.configuration import DatabaseConfig
from appkit_commons.database.entities import Base, Entity
from appkit_commons.registry import service_registry
from appkit_commons.security import check_password_hash, generate_password_hash

logger = logging.getLogger(__name__)
db_config: DatabaseConfig = service_registry().get(DatabaseConfig)

SECRET_VALUE: Final = db_config.encryption_key.get_secret_value()


class UserEntity(Entity, Base):
    """User model with relationships to roles and OAuth accounts."""

    __tablename__ = "auth_users"

    email: Mapped[str | None] = mapped_column(String(200), nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    _password: Mapped[str] = mapped_column(String(200), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    needs_password_reset: Mapped[bool] = mapped_column(Boolean, default=False)
    roles: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list, nullable=False
    )
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    oauth_accounts: Mapped[list["OAuthAccountEntity"]] = relationship(
        "OAuthAccountEntity",
        back_populates="user",
        lazy="select",
        cascade="all, delete-orphan",
    )
    oauth_states: Mapped[list["OAuthStateEntity"]] = relationship(
        "OAuthStateEntity",
        back_populates="user",
        lazy="select",
        cascade="all, delete-orphan",
    )
    sessions: Mapped[list["UserSessionEntity"]] = relationship(
        "UserSessionEntity",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    @property
    def password(self) -> str:
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        self._password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self._password, password)

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "user_id": self.id,
            "email": self.email,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "needs_password_reset": self.needs_password_reset,
            "roles": self.roles,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }


class UserSessionEntity(Entity, Base):
    """User session model for tracking user sessions."""

    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("auth_users.id", ondelete="CASCADE"),
        nullable=False,
    )
    session_id: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Relationships
    user: Mapped["UserEntity"] = relationship(
        back_populates="sessions", lazy="selectin"
    )

    def is_expired(self) -> bool:
        """Check if the session is expired."""
        # Ensure both datetimes are offset-aware for comparison
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        now = datetime.now(UTC)
        return now >= expires_at

    def to_dict(self) -> dict[str, str | int]:
        """Convert session to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "expires_at": self.expires_at.isoformat(),
        }


class OAuthAccountEntity(Entity, Base):
    """OAuth account linking users to external providers with token management."""

    __tablename__ = "auth_oauth_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("auth_users.id", ondelete="CASCADE"),
        nullable=False,
    )
    provider: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., "github", "azure"
    account_id: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # Provider's user ID
    account_email: Mapped[str] = mapped_column(
        String(200), nullable=False
    )  # Provider's email
    access_token: Mapped[str] = mapped_column(
        StringEncryptedType(Unicode, SECRET_VALUE, FernetEngine)
    )
    refresh_token: Mapped[str | None] = mapped_column(
        StringEncryptedType(Unicode, SECRET_VALUE, FernetEngine)
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )  # Token expiration
    token_type: Mapped[str] = mapped_column(String(20), default="Bearer")
    scope: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    user: Mapped["UserEntity"] = relationship(back_populates="oauth_accounts")

    __table_args__ = (
        UniqueConstraint("provider", "account_id", name="uq_oauth_provider_account"),
        Index("ix_oauth_accounts_user_id", "user_id"),
    )


class OAuthStateEntity(Entity, Base):
    """OAuth state for CSRF protection with session management."""

    __tablename__ = "auth_oauth_states"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("auth_users.id", ondelete="SET NULL"),
        nullable=True,
    )
    session_id: Mapped[str] = mapped_column(String(200), nullable=False)
    state: Mapped[str] = mapped_column(String(200), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    # PKCE code_verifier tied to the state (nullable for providers not using PKCE)
    code_verifier: Mapped[str | None] = mapped_column(String(200), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )  # OAuth state expiration

    user: Mapped[Optional["UserEntity"]] = relationship(
        "UserEntity", back_populates="oauth_states", lazy="select"
    )

    __table_args__ = (Index("ix_oauth_states_expires_at", "expires_at"),)
