# MCP Builder - Production-Ready Dockerfile with UV
# Multi-stage build optimized for fast builds and minimal final image size

# Build stage - Install dependencies
FROM python:3.12-slim-bookworm AS builder

# Install UV from official image - pinned to specific version for reproducibility
COPY --from=ghcr.io/astral-sh/uv:0.5.18 /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Set UV environment variables for optimal Docker usage
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/root/.cache/uv

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies only (not the project itself) with cache mount
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable

# Production stage - Final runtime image
FROM python:3.12-slim-bookworm AS production

# Create non-root user for security
RUN groupadd -r mcp && useradd -r -g mcp mcp

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder --chown=mcp:mcp /app/.venv /app/.venv

# Copy application source code
COPY --chown=mcp:mcp src/ ./src/
COPY --chown=mcp:mcp pyproject.toml ./

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy UV binary to production stage for project installation
COPY --from=ghcr.io/astral-sh/uv:0.5.18 /uv /uvx /bin/

# Install the project itself using UV
RUN /bin/uv pip install --no-deps -e . --python /app/.venv/bin/python

# Switch to non-root user
USER mcp

# Health check for MCP server
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Set default environment variables for MCP server
ENV MCP_HELLO_TRANSPORT_TYPE=stdio
ENV MCP_HELLO_LOG_LEVEL=INFO
ENV MCP_HELLO_DEBUG_MODE=false

# Expose port for SSE/WebSocket transports (if needed)
EXPOSE 8000

# Default command runs the main MCP server
CMD ["python", "src/server.py"]

# Development stage - For development with hot reloading
FROM builder AS development

# Copy source code first for development builds
COPY src/ ./src/

# Install development dependencies including the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set development environment variables
ENV MCP_HELLO_DEBUG_MODE=true
ENV MCP_HELLO_LOG_LEVEL=DEBUG

# Development command with file watching
CMD ["python", "src/server.py"]