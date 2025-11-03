# Common Utilities

This module provides common utility functions used across the application to ensure consistency and eliminate code duplication.

## Overview

The `appkit_commons.utils` module centralizes frequently used utility functions that were previously scattered across different modules, particularly in authentication and user management.

## Modules

### `datetime_utils` - Date and Time Helpers

Provides consistent UTC datetime handling utilities.

#### Functions

**`get_current_utc_time()`**
- Returns current datetime in UTC timezone
- Ensures consistent timezone handling across the application

**Example:**
```python
from appkit_commons.utils import get_current_utc_time

now = get_current_utc_time()
user.last_login = now
```

**`get_expiration_time(seconds)`**
- Calculates expiration datetime by adding seconds to current UTC time
- Normalizes seconds and microseconds to 0 for cleaner timestamps
- Useful for session expiration, token expiration, etc.

**Example:**
```python
from appkit_commons.utils import get_expiration_time

# Session expires in 1 hour
session_expires = get_expiration_time(3600)

# Token expires in 30 minutes
token_expires = get_expiration_time(1800)
```

### `string_utils` - String Processing Helpers

Provides common string manipulation and normalization utilities.

#### Functions

**`normalize_scope(scope_data)`**
- Normalizes OAuth scope data to consistent string format
- Handles multiple input types: list, string, or None
- Returns space-separated string for lists

**Example:**
```python
from appkit_commons.utils import normalize_scope

# List to space-separated string
scopes = normalize_scope(["read", "write", "admin"])
# Result: "read write admin"

# String passes through unchanged
scopes = normalize_scope("read write")
# Result: "read write"

# None stays None
scopes = normalize_scope(None)
# Result: None
```

**`get_name_from_email(email, fallback_name=None)`**
- Extracts username from email address when name is not available
- Uses fallback name if provided and non-empty
- Falls back to email local part (before @) if no name given

**Example:**
```python
from appkit_commons.utils import get_name_from_email

# Extract from email when no fallback
name = get_name_from_email("john.doe@example.com")
# Result: "john.doe"

# Use fallback when provided
name = get_name_from_email("john@example.com", "John Doe")
# Result: "John Doe"

# Use email when fallback is empty
name = get_name_from_email("jane@example.com", "")
# Result: "jane"
```

## Usage Pattern

### Before (duplicated utilities):
```python
# In user_repository.py
def get_current_utc_time() -> datetime:
    return datetime.now(UTC)

def normalize_scope(scope_data: Any) -> str | None:
    if isinstance(scope_data, list):
        return " ".join(scope_data)
    # ... more logic
```

### After (using common utilities):
```python
from appkit_commons.utils import (
    get_current_utc_time,
    normalize_scope,
)

# Use directly in your code
user.last_login = get_current_utc_time()
scopes = normalize_scope(oauth_scopes)
```

## Benefits

1. **Consistency**: Ensures datetime handling is uniform across the application
2. **DRY Principle**: Eliminates duplicate utility function definitions
3. **Maintainability**: Changes to common logic only need to be made once
4. **Testability**: Common utilities can be unit tested independently
5. **Type Safety**: Proper type hints maintained throughout

## Modules Refactored

The following modules have been refactored to use these utilities:

- ✅ `user_repository.py` - Removed 4 duplicate helper functions

## Design Notes

### UTC-First Approach

All datetime utilities use UTC timezone by default to ensure:
- Consistent timestamps across different server locations
- Proper sorting and comparison of datetimes
- Avoidance of daylight saving time issues

### Flexible String Handling

String utilities handle multiple input types gracefully:
- Accept lists, strings, or None
- Return appropriate types for each case
- Never raise exceptions for invalid input

## Future Enhancements

Potential future utilities to add:
- Email validation and normalization
- Phone number formatting
- Currency formatting helpers
- File size formatting
- URL validation and parsing
