# ────────────────────────────  Stage 1 ─ Builder  ────────────────────────────
ARG VARIANT=3.13-slim-bookworm
FROM python:${VARIANT} AS builder

# Stage 1: Install required libraries
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y upgrade \
    && apt-get -y install --no-install-recommends postgresql-client libpq-dev caddy unzip curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# ───────────────────────────  Stage 2 ─ Runtime  ────────────────────────────
FROM builder AS final

ARG PORT=80
ARG BACKEND_PORT=3030
ARG API_URL
ENV PORT=$PORT REFLEX_API_URL=${API_URL:-http://localhost:$PORT}

ENV WORK=/reflexapp
WORKDIR ${WORK}

# Copy project configuration files first for better caching
COPY pyproject.toml uv.lock .python-version alembic.ini README.md start.sh Caddyfile ${WORK}/

# Copy all source code including workspace members
COPY rxconfig.py ${WORK}/
COPY configuration ${WORK}/configuration
COPY assets ${WORK}/assets
COPY alembic ${WORK}/alembic
COPY components ${WORK}/components
COPY app ${WORK}/app

# Install dependencies using uv sync (installs workspace members automatically)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-extras && \
    chmod +x ${WORK}/start.sh

# Expose ports
EXPOSE $PORT $BACKEND_PORT

# Run the application
CMD ["./start.sh"]
