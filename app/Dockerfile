# Stage 1: The Builder
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
WORKDIR /app

# Copy config files from the root
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Stage 2: The Runtime
FROM python:3.13-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Copy the Linux-native venv from the builder
COPY --from=builder /app/.venv /app/.venv

# 2. Copy only the contents of the 'app' folder into our container's /app
# This ensures main.py is at /app/main.py, not /app/app/main.py
COPY app/ .

# 3. Add the venv to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Now we can just call 'uvicorn' directly because it's in the PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]