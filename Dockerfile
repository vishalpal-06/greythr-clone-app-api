############################
# Builder stage
############################
FROM python:3.12-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Copy dependency metadata first
COPY pyproject.toml uv.lock ./

# Install only production dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --locked \
    --no-install-project \
    --no-dev


############################
# Runtime stage
############################
FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    DB_CONNECT="local"

WORKDIR /app

# Install latest available OS security updates
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --system --gid 1001 appgroup \
    && useradd \
        --system \
        --uid 1001 \
        --gid appgroup \
        --no-create-home \
        appuser

# Copy production virtual environment
COPY --from=builder --chown=appuser:appgroup \
    /app/.venv \
    /app/.venv

# Copy application code
COPY --chown=appuser:appgroup main.py ./
COPY --chown=appuser:appgroup common ./common
COPY --chown=appuser:appgroup database ./database
COPY --chown=appuser:appgroup routers ./routers
COPY --chown=appuser:appgroup schema ./schema

# Alembic migration files
COPY --chown=appuser:appgroup alembic ./alembic

# Alembic config lives in pyproject.toml
COPY --chown=appuser:appgroup pyproject.toml ./

# Copy local SQLite database
COPY --chown=appuser:appgroup greythr.db ./greythr.db

# SQLite needs write access to:
# 1. database file
# 2. parent directory for journal/WAL files
RUN chown -R appuser:appgroup /app \
    && chmod 775 /app \
    && chmod 664 /app/greythr.db

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
