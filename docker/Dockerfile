# syntax=docker/dockerfile:1.9

############################################################
# GLOBAL ARGs (with defaults) — apply to all stages
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
# BUILDER STAGE — install Python via uv, then deps via uv
############################################################
FROM ${BASE_IMAGE} AS builder
LABEL org.opencontainers.image.source="https://github.com/<OWNER>/<REPO>"

# Bring in uv & uvx
COPY --from=uvbin /uv /uv
COPY --from=uvbin /uvx /uvx
ENV PATH="/:${PATH}" \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl git libssl-dev libffi-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml ./

# Generate lock and sync dependencies
RUN --mount=type=cache,target=/root/.cache \
    uv lock && \
    if [ "$MODE" = "dev" ]; then \
    uv sync --locked --extra ${EXTRA} --group default,dev && \
    uv compile /app/.venv/lib/python*/site-packages; \
    else \
    uv sync --locked --extra ${EXTRA} --group default; \
    fi

############################################################
# FINAL STAGE — runtime image
############################################################
# Re-declare BASE_IMAGE (no default) so Docker picks up the previous value
ARG BASE_IMAGE
ARG MODE

FROM ${BASE_IMAGE} AS final
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

# Runtime-only libs
RUN apt-get update && \
    apt-get install -y --no-install-recommends libssl1.1 && \
    rm -rf /var/lib/apt/lists/*

# Copy the completed venv from builder
COPY --from=builder /app/.venv /app/.venv

# In prod, drop to non-root
RUN if [ "$MODE" = "prod" ]; then \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app/.venv; \
    fi

WORKDIR /app
USER ${MODE:+appuser}

CMD ["python"]
