"""Common date and time utilities for the application.

This module provides centralized date/time handling utilities to ensure
consistency across the application.
"""

from datetime import UTC, datetime, timedelta


def get_current_utc_time() -> datetime:
    """Get current UTC time.

    Returns:
        Current datetime in UTC timezone

    Example:
        ```python
        from appkit_commons.utils.datetime_utils import get_current_utc_time

        now = get_current_utc_time()
        print(now)  # 2024-01-15 10:30:00+00:00
        ```
    """
    return datetime.now(UTC)


def get_expiration_time(seconds: int) -> datetime:
    """Calculate expiration time from seconds.

    Creates an expiration datetime by adding the specified seconds to the
    current UTC time, with seconds and microseconds normalized to 0.

    Args:
        seconds: Number of seconds until expiration

    Returns:
        Datetime representing the expiration time

    Example:
        ```python
        from appkit_commons.utils.datetime_utils import get_expiration_time

        # Get expiration time for a 1-hour session
        expires_at = get_expiration_time(3600)
        ```
    """
    base_time = get_current_utc_time().replace(second=0, microsecond=0)
    return base_time + timedelta(seconds=seconds)
