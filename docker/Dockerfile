# syntax=docker/dockerfile:1.9

############################################################
# GLOBAL ARGs (with defaults)
############################################################
ARG BASE_IMAGE=debian:bullseye-slim
ARG PYTHON_VERSION=3.12
ARG EXTRA=cpu        # "cpu" or "cu124"
ARG MODE=dev         # "dev" or "prod"

############################################################
# UV HELPER STAGE — grab uv & uvx binaries
############################################################
FROM ghcr.io/astral-sh/uv:0.7.6 AS uvbin

############################################################
# BUILDER STAGE
############################################################
FROM ${BASE_IMAGE} AS builder

# Bring build args into scope
ARG PYTHON_VERSION
ARG EXTRA
ARG MODE

LABEL org.opencontainers.image.source="https://github.com/<OWNER>/<REPO>"

# Import uv & uvx
COPY --from=uvbin /uv /uv
COPY --from=uvbin /uvx /uvx
ENV PATH="/:${PATH}" \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# OS deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl git libssl-dev libffi-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml ./

# 1️⃣ Install Python interpreter via uv
RUN --mount=type=cache,target=/root/.cache \
    uv python install ${PYTHON_VERSION} --preview --default

# 2️⃣ Generate lock, sync & precompile (in dev)
RUN --mount=type=cache,target=/root/.cache \
    uv lock && \
    if [ "$MODE" = "dev" ]; then \
    uv sync --locked --extra ${EXTRA} --group default,dev && \
    uv compile /app/.venv/lib/python*/site-packages; \
    else \
    uv sync --locked --extra ${EXTRA} --group default; \
    fi

############################################################
# FINAL STAGE
############################################################
ARG BASE_IMAGE
ARG MODE
FROM ${BASE_IMAGE} AS final

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

# Runtime libs only
RUN apt-get update && \
    apt-get install -y --no-install-recommends libssl1.1 && \
    rm -rf /var/lib/apt/lists/*

# Copy in the venv from builder
COPY --from=builder /app/.venv /app/.venv

# Drop to non-root in prod
RUN if [ "$MODE" = "prod" ]; then \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app/.venv; \
    fi

WORKDIR /app
USER ${MODE:+appuser}

CMD ["python"]
