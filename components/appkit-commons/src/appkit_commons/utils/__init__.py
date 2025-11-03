"""Common utility modules for the application."""

from appkit_commons.utils.datetime_utils import (
    get_current_utc_time,
    get_expiration_time,
)
from appkit_commons.utils.string_utils import (
    get_name_from_email,
    normalize_scope,
)

__all__ = [
    "get_current_utc_time",
    "get_expiration_time",
    "get_name_from_email",
    "normalize_scope",
]
