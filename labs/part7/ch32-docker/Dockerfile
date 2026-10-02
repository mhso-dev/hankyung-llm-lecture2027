# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:0.12.13 AS uv-bin

FROM python:3.12-slim-bookworm AS builder
COPY --from=uv-bin /uv /uvx /bin/
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

FROM python:3.12-slim-bookworm AS runtime
WORKDIR /app
RUN groupadd --system course && useradd --system --gid course course
COPY --from=builder --chown=course:course /app/.venv /app/.venv
COPY --chown=course:course app.py ./app.py
ENV PATH="/app/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER course
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=2s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
