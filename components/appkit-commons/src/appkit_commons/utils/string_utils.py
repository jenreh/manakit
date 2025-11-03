"""Common string utilities for the application."""

from typing import Any


def normalize_scope(scope_data: Any) -> str | None:
    """Normalize scope data to string format.

    Handles multiple input types for OAuth scopes and normalizes them to
    a space-separated string format.

    Args:
        scope_data: Scope data in various formats (list, string, or None)

    Returns:
        Normalized scope string or None

    Example:
        ```python
        from appkit_commons.utils.string_utils import normalize_scope

        # List to space-separated string
        assert normalize_scope(["read", "write"]) == "read write"

        # String remains unchanged
        assert normalize_scope("read write") == "read write"

        # None returns None
        assert normalize_scope(None) is None
        ```
    """
    if isinstance(scope_data, list):
        return " ".join(scope_data)
    if scope_data is not None:
        return str(scope_data)
    return None


def get_name_from_email(
    email: str | None, fallback_name: str | None = None
) -> str | None:
    """Extract name from email address if name is empty or None.

    Uses the local part of the email (before @) as the name if no
    fallback name is provided or if the fallback is empty.

    Args:
        email: Email address to extract name from
        fallback_name: Optional name to use instead of extracting from email

    Returns:
        Extracted or fallback name, or None

    Example:
        ```python
        from appkit_commons.utils.string_utils import get_name_from_email

        # Extract from email when no fallback
        assert get_name_from_email("john.doe@example.com") == "john.doe"

        # Use fallback when provided
        assert get_name_from_email("john@example.com", "John Doe") == "John Doe"

        # Use email when fallback is empty
        assert get_name_from_email("jane@example.com", "") == "jane"
        ```
    """
    if fallback_name and fallback_name.strip():
        return fallback_name
    if email and "@" in email:
        return email.split("@")[0]
    return fallback_name
