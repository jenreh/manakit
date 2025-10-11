ARG VARIANT=3.13-bookworm
FROM mcr.microsoft.com/devcontainers/python:${VARIANT} AS base

ENV PATH="/root/.local/bin/:$PATH" \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Stage 1: Install UV separately to optimize caching
#RUN curl -LsSf https://astral.sh/uv/install.sh | sh
