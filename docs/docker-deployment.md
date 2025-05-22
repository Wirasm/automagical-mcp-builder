# MCP Builder - Docker Deployment Guide

This guide covers containerized deployment of MCP servers using Docker and UV package manager.

## Overview

The MCP Builder template includes production-ready Docker configuration with:
- **Multi-stage builds** for optimized image size and build performance
- **UV package manager** integration for fast dependency management
- **Multiple deployment modes** (stdio, SSE, WebSocket)
- **Development and production configurations**
- **Comprehensive health checks and monitoring**

## Quick Start

### 1. Build and Run (Development)

```bash
# Build Docker images
./scripts/docker-run.sh build

# Start development server with hot reloading
./scripts/docker-run.sh dev

# Or run in background
./scripts/docker-run.sh dev --detach
```

### 2. Production Deployment

```bash
# Start production server
./scripts/docker-run.sh prod --detach

# Start SSE server for web integrations
./scripts/docker-run.sh sse --detach
```

### 3. Testing

```bash
# Run tests in container
./scripts/docker-run.sh test

# Get shell access for debugging
./scripts/docker-run.sh shell dev
```

## Docker Architecture

### Multi-Stage Build

```dockerfile
# Stage 1: Builder - Install dependencies with UV
FROM python:3.12-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.18 /uv /uvx /bin/

# Stage 2: Production - Minimal runtime image
FROM python:3.12-slim-bookworm AS production
COPY --from=builder /app/.venv /app/.venv

# Stage 3: Development - Full tooling for development
FROM builder AS development
# Development-specific setup
```

### Key Optimizations

**UV Package Manager Integration:**
- Pinned UV version for reproducibility
- Cache mounts for faster builds (`--mount=type=cache,target=/root/.cache/uv`)
- Separate dependency and project installation
- Bytecode compilation for faster startup

**Security:**
- Non-root user execution
- Minimal base images (slim-bookworm)
- Resource limits and health checks

**Performance:**
- Layer caching optimization
- Multi-stage builds for minimal final image
- Dependency caching between builds

## Deployment Modes

### 1. Stdio Transport (Default)

For Claude Desktop and local MCP clients:

```bash
docker run -it mcp-builder:latest
```

**Environment Variables:**
```bash
MCP_HELLO_TRANSPORT_TYPE=stdio
MCP_HELLO_LOG_LEVEL=INFO
```

### 2. SSE Transport

For web-based integrations:

```bash
docker run -p 8000:8000 -e MCP_HELLO_TRANSPORT_TYPE=sse mcp-builder:latest
```

**Access:** `http://localhost:8000/sse`

### 3. WebSocket Transport

For real-time applications:

```bash
docker run -p 8001:8001 -e MCP_HELLO_TRANSPORT_TYPE=websocket -e MCP_HELLO_PORT=8001 mcp-builder:latest
```

**Access:** `ws://localhost:8001/ws`

## Configuration

### Environment Variables

All MCP server configuration can be controlled via environment variables:

```bash
# Server Configuration
MCP_HELLO_SERVER_NAME="My MCP Server"
MCP_HELLO_VERSION="1.0.0"
MCP_HELLO_TRANSPORT_TYPE=stdio|sse|websocket

# Network Configuration (SSE/WebSocket)
MCP_HELLO_HOST=0.0.0.0
MCP_HELLO_PORT=8000

# Logging Configuration
MCP_HELLO_LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
MCP_HELLO_DEBUG_MODE=true|false

# Feature Toggles
MCP_HELLO_ENABLE_GREETING_TOOL=true
MCP_HELLO_ENABLE_SERVER_INFO_TOOL=true
MCP_HELLO_ENABLE_STATUS_RESOURCE=true
# ... additional feature flags
```

### Docker Compose Configuration

The `docker-compose.yml` provides pre-configured services:

```yaml
services:
  mcp-server:        # Production stdio server
  mcp-server-sse:    # Production SSE server
  mcp-server-dev:    # Development server with hot reloading
  mcp-server-test:   # Testing service
```

## Production Deployment

### 1. Basic Production Setup

```bash
# Clone and setup
git clone <repository>
cd mcp-builder

# Build production images
./scripts/docker-run.sh build

# Start production services
docker-compose up -d mcp-server mcp-server-sse
```

### 2. Health Monitoring

Built-in health checks:

```bash
# Check container health
docker ps

# View health check logs
docker inspect mcp-server --format='{{.State.Health.Status}}'

# Manual health check
docker exec mcp-server python -c "import sys; sys.exit(0)"
```

### 3. Log Management

```bash
# View live logs
./scripts/docker-run.sh logs

# Persistent logging with volume mounts
docker-compose up -d  # Logs saved to ./logs/
```

### 4. Resource Management

Resource limits are configured in docker-compose.yml:

```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
    reservations:
      memory: 256M
      cpus: '0.25'
```

## Development Workflow

### 1. Development Server

Hot reloading development setup:

```bash
# Start development server
./scripts/docker-run.sh dev

# Source code changes automatically reflected
# No need to rebuild container
```

### 2. Testing

Containerized testing:

```bash
# Run all tests
./scripts/docker-run.sh test

# Interactive testing
./scripts/docker-run.sh shell dev
pytest src/ -v
```

### 3. Debugging

```bash
# Get shell access
./scripts/docker-run.sh shell dev

# Debug specific container
docker-compose exec mcp-server-dev /bin/bash

# View container logs
docker-compose logs -f mcp-server-dev
```

## Cloud Deployment

### 1. Container Registry

Push to container registry:

```bash
# Build and tag
docker build -t your-registry/mcp-builder:latest .

# Push to registry
docker push your-registry/mcp-builder:latest
```

### 2. Kubernetes Deployment

Example Kubernetes configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: your-registry/mcp-builder:latest
        ports:
        - containerPort: 8000
        env:
        - name: MCP_HELLO_TRANSPORT_TYPE
          value: "sse"
        - name: MCP_HELLO_LOG_LEVEL
          value: "INFO"
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
        healthcheck:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### 3. Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml mcp-stack
```

## Troubleshooting

### Common Issues

**1. Build Failures**
```bash
# Clean build
./scripts/docker-run.sh build --rebuild

# Check logs
docker build --progress=plain .
```

**2. Container Won't Start**
```bash
# Check logs
docker logs mcp-server

# Debug startup
docker run --rm -it mcp-builder:latest /bin/bash
```

**3. Permission Issues**
```bash
# Check user permissions
docker exec mcp-server id

# Fix file ownership
sudo chown -R $(id -u):$(id -g) logs/
```

**4. Memory Issues**
```bash
# Check resource usage
docker stats

# Increase memory limits in docker-compose.yml
```

### Validation

Test your Docker setup:

```bash
# Comprehensive validation
./scripts/docker-run.sh validate

# Manual validation steps
docker build . -t test
docker run --rm test python -c "import src.server; print('OK')"
```

## Performance Optimization

### 1. Build Performance

- Use cache mounts for UV dependencies
- Optimize layer ordering in Dockerfile
- Use .dockerignore to reduce build context

### 2. Runtime Performance

- Enable bytecode compilation (`UV_COMPILE_BYTECODE=1`)
- Use appropriate resource limits
- Monitor container metrics

### 3. Storage Optimization

- Multi-stage builds reduce final image size
- Use slim base images
- Remove unnecessary dependencies

## Security Considerations

### 1. Container Security

- Run as non-root user
- Use minimal base images
- Regular security updates

### 2. Network Security

- Expose only necessary ports
- Use proper firewall configuration
- Consider TLS for production

### 3. Secrets Management

```bash
# Use Docker secrets for sensitive data
echo "api_key_value" | docker secret create api_key -

# Reference in docker-compose.yml
secrets:
  - api_key
```

## Monitoring and Observability

### 1. Logging

Structured logging is configured by default:

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "INFO",
  "service": "mcp-builder",
  "message": "Tool execution completed",
  "tool_name": "greeting",
  "duration_ms": 150
}
```

### 2. Metrics

Monitor container metrics:

```bash
# Resource usage
docker stats mcp-server

# Health status
docker inspect mcp-server --format='{{.State.Health}}'
```

### 3. Alerts

Configure alerts based on:
- Container health status
- Resource usage thresholds
- Log error patterns
- Response time metrics

This Docker deployment setup provides a production-ready foundation for deploying MCP servers with enterprise-grade reliability, security, and monitoring capabilities.