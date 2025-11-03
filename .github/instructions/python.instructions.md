---
applyTo: '**/*.py'
description: 'Python development guidelines and best practices for the appkit project'
---

# Python Development Instructions

## Project Overview

This is a **Python 3.13** project using:
- **Reflex** - Web framework for building reactive UIs
- **FastAPI** - High-performance web framework
- **SQLAlchemy 2.0** - Database ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **uv** - Package and project manager

## Setup and Installation

```bash
# Install dependencies
make install
# or
uv sync
```

## Development Workflow

### Running the Application

```bash
# Start development server
make reflex
# or
uv run reflex run

# Start with debug logging
make reflex-debug
# or
uv run reflex run --loglevel=debug

# Production mode
make reflex-prod
# or
uv run reflex run --env prod
```

### Testing

```bash
# Run tests
make test
# or
uv run pytest

# Run tests with coverage
uv run pytest --cov=app --cov=appkit_assistant --cov=appkit_commons --cov=appkit_imagecreator --cov=appkit_mantine --cov=appkit_ui --cov=appkit_user
```

**Note:** Tests should be written in `tests/` directory following the pattern `test_*.py`.

### Linting and Formatting

```bash
# Check code style
make check
# or
uv run ruff check .
uv run ruff format --check .

# Auto-fix linting issues
make lint
# or
uv run ruff check --fix .

# Format code
make format
# or
uv run ruff format .
uv run ruff check --fix .
```

### Database Migrations

```bash
# Check current migration status
make alembic
# or
uv run alembic current

# Apply migrations
make db-migrate
# or
uv run alembic upgrade head

# View migration history
make db-migrate-history
# or
uv run alembic history

# Rollback one migration
make db-migrate-down
# or
uv run alembic downgrade -1
```

## Code Style Guidelines

### Logging

**CRITICAL:** Never use f-strings in logger calls. Use string formatting with parameters instead.

```python
import logging

log = logging.getLogger(__name__)

# ✅ CORRECT
log.info("Loaded items: %d", count)
log.error("Failed to process user: %s", user_id)
log.debug("Processing request with params: %s, %s", param1, param2)

# ❌ INCORRECT - DO NOT USE
log.info(f"Loaded items: {count}")
log.error(f"Failed to process user: {user_id}")
```

### Type Annotations

All functions should have proper type annotations:

```python
from typing import Any, AsyncGenerator, Literal
from reflex.vars.base import Var
from reflex.event import EventHandler

def process_data(data: dict[str, Any], count: int = 0) -> list[str]:
    """Process data and return list of strings."""
    pass

async def async_handler(value: str) -> AsyncGenerator[Any, Any]:
    """Async event handler."""
    yield
```

### Reflex Components

Follow these patterns for Reflex components:

```python
import reflex as rx

# Separate state from view
class MyState(rx.State):
    value: str = ""
    error: str = ""
    
    def set_value(self, val: str) -> None:
        """Set value with validation."""
        self.value = val
    
    @rx.event
    async def validate(self) -> AsyncGenerator[Any, Any]:
        """Validate and show toast."""
        if not self.value:
            self.error = "Value is required"
        else:
            self.error = ""
            yield rx.toast.success("Valid!", position="top-right")

# Small, focused components
def my_component() -> rx.Component:
    """Component documentation."""
    return rx.container(
        rx.input(
            value=MyState.value,
            on_change=MyState.set_value,
        ),
    )
```

## Testing Guidelines

### Test Structure

```python
import pytest
from app.module import function_to_test

def test_function_basic_case() -> None:
    """Test basic functionality."""
    result = function_to_test("input")
    assert result == "expected"

def test_function_edge_case() -> None:
    """Test edge case."""
    result = function_to_test("")
    assert result == ""

@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Provide sample data for tests."""
    return {"key": "value"}

def test_with_fixture(sample_data: dict[str, Any]) -> None:
    """Test using fixture."""
    assert sample_data["key"] == "value"
```

### Coverage Requirements

- Target: **≥ 80% code coverage**
- All new features must include tests
- Bug fixes should include regression tests

## Security Best Practices

1. **Secrets Management**
   - Never commit credentials, API keys, or secrets to version control
   - Use `.env` files locally (excluded via `.gitignore`)
   - Use Azure Key Vault or environment variables in production

2. **Input Validation**
   - Always validate user input using Pydantic models
   - Sanitize data before database operations

3. **Dependency Updates**
   - Keep dependencies up to date
   - Document security-related updates in commit messages
   - Use `uv lock --upgrade` to update dependencies

## Common Patterns

### State Management with Validation

```python
class FormState(rx.State):
    username: str = ""
    username_error: str = ""
    
    @rx.event
    async def validate_username(self) -> AsyncGenerator[Any, Any]:
        """Validate username field."""
        if len(self.username) < 3:
            self.username_error = "Must be at least 3 characters"
        else:
            self.username_error = ""
            yield rx.toast.success("Valid username!", position="top-right")
```

### Database Operations

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    """Get user by ID."""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

## Pre-Commit Checklist

Before committing code, ensure:

- [ ] Tests pass: `make test`
- [ ] Linting passes: `make check`
- [ ] Code is formatted: `make format`
- [ ] Coverage ≥ 80%
- [ ] No secrets or credentials in code
- [ ] Logging uses parameter formatting (not f-strings)
- [ ] All functions have type annotations
- [ ] Documentation updated if needed

## Conventional Commits

Use conventional commit messages:

```bash
feat: add new user authentication component
fix: resolve database connection pooling issue
refactor: simplify state management in forms
docs: update API documentation
test: add tests for user validation
chore: update dependencies
```

## File Organization

```
appkit/
├── app/                    # Main application
│   ├── components/        # Reusable UI components
│   └── pages/            # Page components
├── components/            # Workspace packages
│   ├── appkit-assistant/
│   ├── appkit-commons/
│   ├── appkit-imagecreator/
│   ├── appkit-mantine/   # Mantine UI wrappers
│   ├── appkit-ui/
│   └── appkit-user/
├── alembic/              # Database migrations
├── configuration/        # Config files
└── tests/               # Test files
```

## Additional Resources

- [Reflex Documentation](https://reflex.dev/docs/)
- [Mantine UI Documentation](https://mantine.dev)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
