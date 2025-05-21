# syntax=docker/dockerfile:1.9

############################################################
# BUILDER STAGE
############################################################
ARG BASE_IMAGE
ARG PYTHON_VERSION=3.12
ARG EXTRA=cpu        # cpu or cu124
ARG MODE=prod        # dev or prod

FROM ${BASE_IMAGE} AS builder
LABEL org.opencontainers.image.source="https://github.com/<OWNER>/<REPO>"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/app \
    UV_LINK_MODE=copy \
    PATH="/root/.cargo/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git libssl-dev libffi-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" \
    | tar xz && cd Python-${PYTHON_VERSION} \
    && ./configure --enable-optimizations \
    && make -j$(nproc) install \
    && cd .. && rm -rf Python-${PYTHON_VERSION}*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache \
    if [ "$MODE" = "dev" ]; then \
    uv sync --locked --extra ${EXTRA} --group default,dev && \
    uv compile /app/.venv/lib/python*/site-packages; \
    else \
    uv sync --locked --extra ${EXTRA} --group default; \
    fi

############################################################
# FINAL STAGE
############################################################
FROM ${BASE_IMAGE}
ARG PYTHON_VERSION
ARG MODE

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl1.1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv

RUN if [ "$MODE" = "prod" ]; then \
    useradd -m -u 1000 appuser && chown -R appuser:appuser /app/.venv; \
    fi

WORKDIR /app
USER ${MODE:+appuser}
CMD ["python"]
