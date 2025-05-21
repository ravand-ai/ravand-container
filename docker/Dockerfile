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
# BUILDER STAGE — install Python via uv, then deps via uv
############################################################
FROM ${BASE_IMAGE} AS builder

# Bring build args into this stage’s scope
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

# Install OS packages needed for uv and Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl git libssl-dev libffi-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml ./

# 1️⃣ Install the requested Python interpreter via uv
RUN --mount=type=cache,target=/root/.cache \
    uv python install ${PYTHON_VERSION} --preview --default

# 2️⃣ Generate lockfile and install dependencies (CPU or CUDA)
RUN --mount=type=cache,target=/root/.cache \
    uv lock && \
    uv sync --locked --extra ${EXTRA}


############################################################
# FINAL STAGE — runtime image with conditional SSL libs
############################################################
# Re-declare BASE_IMAGE so it’s in scope here
ARG BASE_IMAGE
FROM ${BASE_IMAGE} AS final

# Re-declare MODE for this stage
ARG MODE

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

# Install the appropriate SSL package per distro
RUN apt-get update && \
    if grep -q "Ubuntu 24.04" /etc/os-release; then \
    apt-get install -y --no-install-recommends libssl3; \
    else \
    apt-get install -y --no-install-recommends libssl1.1; \
    fi && \
    rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# In prod mode, switch to a non-root user
RUN if [ "$MODE" = "prod" ]; then \
    useradd -m appuser && \
    chown -R appuser:appuser /app/.venv; \
    fi

WORKDIR /app
USER ${MODE:+appuser}
CMD ["python"]
