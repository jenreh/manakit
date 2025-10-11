# Avvia Intelligence Admin Makefile
# Convenience commands for development

.PHONY: help install server reflex clean test lint format check alembic migrate migrate-auto migrate-history migrate-down setup-azure-providers docker-build docker-tag docker-push docker-login build build-container-app docker-verify docker-config load-env

# Default target
help:
	@echo "Available targets:"
	@echo "  instlal      - Install dependencies using uv"
	@echo "  reflex       - Start the reflex web application"
	@echo "  reflex-debug - Start the reflex web application with logging"
	@echo "  reflex-prod  - Start the reflex web application in prod mode"
	@echo "  clean.       - Clean cache and build artifacts"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting with ruff"
	@echo "  format       - Format code with ruff"
	@echo "  check        - Run linting and formatting checks"
	@echo ""

	@echo "Database commands (Alembic):"
	@echo "  alembic            - Run alembic current (check migration status)"
	@echo "  db-migrate         - Run alembic upgrade head"
	@echo "  db-migrate-history - Show alembic migration history"
	@echo "  db-migrate-down    - Downgrade database by one revision"
	@echo ""

# Install dependencies
install:
	uv sync

# Start the reflex web application
reflex:
	uv run reflex run

# Start the reflex app with debug logging
reflex-debug:
	uv run reflex run --loglevel=debug

# Start the reflex app in production mode
reflex-prod:
	uv run reflex run --env prod

# Clean cache and build artifacts
clean:
	rm -rf __pycache__/
	rm -rf .cache/
	rm -rf .states/
	rm -rf .web/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Run tests
test:
	uv run pytest

# Run linting
lint:
	uv run ruff check .

# Format code
format:
	uv run ruff format .
	uv run ruff check --fix .

# Check linting and formatting
check:
	uv run ruff check .
	uv run ruff format --check .

# Database migration commands (Alembic)
alembic:
	uv run alembic current

db-migrate:
	uv run alembic upgrade head

# Show alembic history
db-migrate-history:
	uv run alembic history

# Downgrade database by one revision
db-migrate-down:
	uv run alembic downgrade -1
