FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

# Copy the project files
COPY . . 

# Install the dependencies
RUN uv sync

# Expose the port
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]