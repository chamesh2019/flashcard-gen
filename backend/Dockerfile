# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

# Set working directory
WORKDIR /app

# Builder stage: install dependencies in a venv
FROM base AS builder

# Copy only requirements.txt first for better cache usage
COPY --link requirements.txt ./

# Create venv and install dependencies using pip cache
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

# Copy application code (excluding files that should not be in the image)
COPY --link app.py ./
COPY --link functions/ ./functions/

# Final stage: copy venv and app, set up non-root user
FROM base AS final

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy venv and app from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app.py ./app.py
COPY --from=builder /app/functions ./functions

# Set environment so venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Set permissions for the non-root user
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
