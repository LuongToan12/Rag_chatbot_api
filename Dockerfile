# Use python 3.12 slim image
FROM python:3.12-slim

# Copy the uv binary from the official ghcr.io image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Enable bytecode compilation and unbuffered logging
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy project files needed for dependency installation
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync with cache mounting
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application files
COPY . .

# Add virtual environment binaries to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]