# MCP Builder Project

## Core Principles

**IMPORTANT: You MUST follow these principles in all code changes:**

### KISS (Keep It Simple, Stupid)
- Simplicity should be a key goal in design
- Choose straightforward solutions over complex ones whenever possible
- Simple solutions are easier to understand, maintain, and debug

### YAGNI (You Aren't Gonna Need It)
- Avoid building functionality on speculation
- Implement features only when they are needed, not when you anticipate they might be useful in the future

### Dependency Inversion
- High-level modules should not depend on low-level modules
- Both should depend on abstractions
- This principle enables flexibility and testability

### Open/Closed Principle
- Software entities should be open for extension but closed for modification
- Design systems so that new functionality can be added with minimal changes to existing code

## UV Package Management

**CRITICAL: This project uses UV for Python package management. NEVER use pip or other package managers.**

### Essential UV Commands
```bash
# Create virtual environment
uv venv

# Install dependencies from pyproject.toml
uv sync

# Install a specific package
uv add requests

# Remove a package
uv remove requests

# Run a Python script or command
uv run python script.py
uv run pytest

# Install editable packages
uv pip install -e .

# Run the main application
uv run python src/main_server.py
```

## Code Architecture

**IMPORTANT: We follow strict vertical slice architecture where each feature is self-contained with co-located tests. Tests MUST be placed directly next to their related feature components.**

### Complete Project Structure
```
├── ai_docs/                    # AI documentation and context
├── claude_desktop_config.json.example # Example Claude Desktop configuration
├── CLAUDE.md                   # This file - project context
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── docs/                       # Documentation
│   └── docker-deployment.md    # Docker deployment guide
├── prps/                       # Product Requirement Prompts
│   └── prp_base_template_v1.md # Base MCP PRP template
├── pyproject.toml              # UV package configuration
├── README.md                   # Project documentation
├── scripts/                    # Utility scripts
│   └── docker-run.sh           # Docker helper script
├── src/                        # Source code
│   ├── __init__.py
│   ├── main_server.py          # Main server entry point (routes to features)
│   ├── logging_config.py       # Standardized logging module
│   ├── data_types.py           # Standard data types and response formats
│   ├── features/               # Feature modules (vertical slices)
│   │   ├── __init__.py
│   │   └── hello_world/        # Hello World example feature
│   │       ├── __init__.py
│   │       ├── config.py       # Feature-specific configuration
│   │       ├── hello_world_server.py # Feature's MCP server implementation
│   │       ├── api/            # External API integrations for this feature
│   │       │   ├── __init__.py
│   │       │   └── tests/      # API tests (currently empty for hello_world)
│   │       │       └── __init__.py
│   │       ├── tools/          # MCP Tools (actions LLMs can call)
│   │       │   ├── __init__.py
│   │       │   ├── greeting.py # Greeting tool implementations
│   │       │   └── tests/      # Tool tests (co-located)
│   │       │       ├── __init__.py
│   │       │       └── test_greeting.py
│   │       ├── resources/      # MCP Resources (read-only data)
│   │       │   ├── __init__.py
│   │       │   ├── status.py   # Status resource implementations
│   │       │   └── tests/      # Resource tests (co-located)
│   │       │       ├── __init__.py
│   │       │       └── test_status.py
│   │       └── prompts/        # MCP Prompts (reusable templates)
│   │           ├── __init__.py
│   │           ├── greeting_template.py # Greeting prompt templates
│   │           └── tests/      # Prompt tests (co-located)
│   │               ├── __init__.py
│   │               └── test_greeting_template.py
│   └── tests/                  # Root-level integration tests
│       ├── __init__.py
│       └── test_logging_config.py # Logging system tests
└── uv.lock                     # Dependency lock file (auto-generated)
```

### Vertical Slice Architecture Rules

**CRITICAL: Every component MUST have its test file in the same directory:**

1. **Tools**: `src/features/feature_name/tools/tool.py` → `src/features/feature_name/tools/tests/test_tool.py`
2. **Resources**: `src/features/feature_name/resources/resource.py` → `src/features/feature_name/resources/tests/test_resource.py`  
3. **Prompts**: `src/features/feature_name/prompts/prompt.py` → `src/features/feature_name/prompts/tests/test_prompt.py`
4. **APIs**: `src/features/feature_name/api/feature_api.py` → `src/features/feature_name/api/tests/test_feature_api.py`

### File Naming Conventions

**IMPORTANT: Follow these naming patterns for clarity and consistency:**

1. **Main Server Entry Point**: `src/main_server.py` - Routes requests to feature servers
2. **Feature Servers**: `src/features/{feature_name}/{feature_name}_server.py` - Individual feature implementations
3. **Feature Config**: `src/features/{feature_name}/config.py` - Feature-specific configuration
4. **Component Files**: Use descriptive names (e.g., `greeting.py`, `status.py`, `greeting_template.py`)
5. **Test Files**: Always prefix with `test_` and match the component name exactly

### Feature Development Pattern

When adding a new MCP server feature (e.g., "github_integration"):

```
src/features/github_integration/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── github_api.py           # GitHub API client
│   └── tests/
│       ├── __init__.py
│       └── test_github_api.py  # Test GitHub API client
├── tools/ 
│   ├── __init__.py
│   ├── create_issue.py         # MCP tool: create GitHub issue
│   ├── get_repo_info.py        # MCP tool: get repository info
│   └── tests/
│       ├── __init__.py
│       ├── test_create_issue.py    # Test create issue tool
│       └── test_get_repo_info.py   # Test repo info tool
├── resources/
│   ├── __init__.py
│   ├── repo_files.py           # MCP resource: repository files
│   └── tests/
│       ├── __init__.py
│       └── test_repo_files.py  # Test repo files resource
└── prompts/
    ├── __init__.py
    ├── code_review.py          # MCP prompt: code review template
    └── tests/
        ├── __init__.py
        └── test_code_review.py # Test code review prompt
```

## Development Commands

### Core Workflow Commands
```bash
# Start development (CRITICAL: Install in editable mode first)
uv sync && uv pip install -e . && uv run python src/main_server.py

# Run tests
uv run pytest

# Run specific test file
uv run pytest tests/test_specific.py

# Run with verbose output
uv run pytest -v

# Format code (if we add formatting tools)
uv run ruff format .

# Lint code (if we add linting tools)  
uv run ruff check .
```

### Testing Strategy - Co-located Tests

**CRITICAL: Tests MUST be placed next to the code they test, not in a separate test directory.**

```bash
# Run all tests
uv run pytest

# Run tests for a specific feature
uv run pytest src/features/github_integration/

# Run tests for a specific component type
uv run pytest src/features/*/tools/tests/

# Run a specific test file
uv run pytest src/features/github_integration/tools/tests/test_create_issue.py

# Run with verbose output to see test structure
uv run pytest -v src/features/
```

### Test Organization Rules

1. **Every .py file MUST have a corresponding test file in the same directory structure**
2. **Test files MUST be in a `tests/` subdirectory next to the code**
3. **Test file names MUST start with `test_` and match the module name**
4. **Each `tests/` directory MUST have `__init__.py`**

### Example Test Commands by Component

```bash
# Test all tools across all features
uv run pytest src/features/*/tools/tests/

# Test all resources across all features  
uv run pytest src/features/*/resources/tests/

# Test all prompts across all features
uv run pytest src/features/*/prompts/tests/

# Test all API integrations across all features
uv run pytest src/features/*/api/tests/

# Test integration (root-level tests)
uv run pytest src/tests/
```

## MCP Development Context

**IMPORTANT: This project builds MCP (Model Context Protocol) servers using our vertical slice architecture.**

### Our MCP Framework Choice
- **Always use FastMCP framework** for high-level MCP server development
- **Only use Python MCP SDK** for low-level protocol customization (rare cases)
- **Follow our feature-based organization** for all MCP servers

### MCP Server Organization in Our Project
Each MCP feature follows our vertical slice pattern:
```
src/features/weather_api/           # Example MCP feature
├── api/                           # External API integration
│   ├── weather_client.py          # API client
│   └── tests/test_weather_client.py
├── tools/                         # MCP Tools (LLM can call)
│   ├── get_forecast.py            # Tool implementation
│   └── tests/test_get_forecast.py # Co-located test
├── resources/                     # MCP Resources (read-only data)
│   ├── current_weather.py         # Resource implementation  
│   └── tests/test_current_weather.py
└── prompts/                       # MCP Prompts (templates)
    ├── weather_summary.py         # Prompt implementation
    └── tests/test_weather_summary.py
```

### MCP Development Commands for Our Project

**CRITICAL: Use these exact commands for MCP development in this project:**

```bash
# Test MCP server during development
uv run mcp dev src/features/{feature_name}/{feature_name}_server.py

# Test with MCP Inspector (visual testing)
npx @modelcontextprotocol/inspector python src/features/{feature_name}/{feature_name}_server.py

# Install MCP server in Claude Desktop for testing
mcp install src/features/{feature_name}/{feature_name}_server.py

# Run MCP-specific tests
uv run pytest src/features/{feature_name}/

# Test all MCP tools across features
uv run pytest src/features/*/tools/tests/

# Test all MCP resources across features  
uv run pytest src/features/*/resources/tests/
```

### MCP Client Integration for Testing

**Claude Desktop Configuration Pattern:**
```json
{
  "mcpServers": {
    "{feature_name}": {
      "command": "uv",
      "args": ["run", "python", "src/features/{feature_name}/{feature_name}_server.py"],
      "cwd": "/absolute/path/to/mcp_builder",
      "env": {
        "API_KEY": "your-api-key-if-needed"
      }
    }
  }
}
```

**Testing Workflow:**
1. Develop MCP server using our vertical slice architecture
2. Test with `uv run mcp dev src/features/{feature}/{feature}_server.py`
3. Validate with MCP Inspector visual testing
4. Integration test with Claude Desktop configuration
5. Run all co-located tests: `uv run pytest src/features/{feature}/`

### MCP Key Concepts (Quick Reference)
- **Tools**: Functions LLMs can call (like POST endpoints) - implement actions
- **Resources**: Read-only data sources (like GET endpoints) - provide data  
- **Prompts**: Reusable templates for LLM interactions - guide usage
- **Transport**: stdio (local testing), SSE (remote deployment)

## Logging Standards

**CRITICAL: All MCP servers MUST use the standardized logging module for consistency and observability.**

### Core Logging Module
Use the centralized logging configuration from `src/logging_config.py`:

```python
from logging_config import setup_mcp_logging, MCPLogger, log_performance, log_context

# Setup logging in your feature's {feature_name}_server.py
logger = setup_mcp_logging(config)

# Use in tools, resources, and prompts
@mcp.tool()
@log_performance(logger)
async def my_tool(param: str) -> str:
    """Tool with automatic performance logging."""
    logger.tool_called("my_tool", param_length=len(param))
    
    try:
        result = process_data(param)
        return success_response(data=result).to_json_string()
    except Exception as e:
        logger.tool_failed("my_tool", str(e), 0)
        return error_response(
            ErrorCode.INTERNAL_ERROR, 
            "Tool execution failed"
        ).to_json_string()
```

### Structured Logging Requirements

**MANDATORY for all MCP implementations:**

1. **Tool Execution Logging**: Every tool MUST log start, completion, and errors
2. **Resource Access Logging**: Track all resource accesses with timing
3. **External API Logging**: Log all external API calls with duration and status
4. **Security Event Logging**: Log authentication and authorization events
5. **Performance Metrics**: Track execution times and resource usage

### Logging Context Management

```python
# Use context for related operations
with log_context(logger, user_id="user123", session_id="session456"):
    result = await some_operation()
    # All logs in this context will include user_id and session_id
```

### Log Levels and Usage

- **DEBUG**: Detailed diagnostic information (development only)
- **INFO**: General information about normal operations
- **WARNING**: Potentially problematic situations that don't stop execution
- **ERROR**: Error events that still allow the application to continue
- **CRITICAL**: Serious error events that may cause the application to abort

## Data Types and Response Standards

**CRITICAL: All MCP servers MUST use standardized data types from `src/data_types.py` for consistency.**

### Standard Response Format

**ALL tools MUST return standardized JSON responses:**

```python
from data_types import MCPToolResponse, success_response, error_response, ErrorCode

@mcp.tool()
async def standardized_tool(name: str) -> str:
    """Tool following standard response format."""
    try:
        # Input validation
        if not name.strip():
            return error_response(
                ErrorCode.VALIDATION_ERROR,
                "Name cannot be empty"
            ).to_json_string()
        
        # Process request
        result = process_name(name)
        
        # Return standardized success
        return success_response(
            data={"processed_name": result},
            message=f"Successfully processed {name}",
            metadata={"processing_time": "0.5s"}
        ).to_json_string()
        
    except Exception as e:
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            f"Processing failed: {str(e)}"
        ).to_json_string()
```

### Input Validation Patterns

**ALL tool inputs MUST be validated using Pydantic models:**

```python
from data_types import TextInput, UserIdentifier, validate_tool_input

@mcp.tool()
async def validated_tool(name: str, email: str = None) -> str:
    """Tool with proper input validation."""
    try:
        # Validate input using standard models
        user_data = validate_tool_input(
            UserIdentifier, 
            {"name": name, "email": email}
        )
        
        # Use validated data
        result = process_user(user_data)
        return success_response(data=result).to_json_string()
        
    except ValueError as e:
        return error_response(
            ErrorCode.VALIDATION_ERROR,
            str(e)
        ).to_json_string()
```

### Resource Data Standards

**ALL resources MUST extend MCPResourceData:**

```python
from data_types import MCPResourceData

class WeatherData(MCPResourceData):
    """Weather resource data model."""
    temperature: float
    humidity: int
    conditions: str
    location: str

@mcp.resource("weather://current/{location}")
async def get_weather(location: str) -> str:
    """Resource with standardized data structure."""
    weather_data = WeatherData(
        temperature=72.5,
        humidity=65,
        conditions="sunny",
        location=location,
        cache_ttl=300  # 5 minutes
    )
    return weather_data.model_dump_json(indent=2)
```

### Error Handling Standards

**ALL errors MUST use standardized error codes and responses:**

```python
from data_types import ErrorCode, error_response

# Standard error patterns:
try:
    api_result = await external_api_call()
except TimeoutError:
    return error_response(
        ErrorCode.TIMEOUT_ERROR,
        "External API request timed out",
        details={"timeout_seconds": 30}
    ).to_json_string()
except PermissionError:
    return error_response(
        ErrorCode.PERMISSION_DENIED,
        "Insufficient permissions for this operation"
    ).to_json_string()
```

### Data Type Rules

**MANDATORY rules for all MCP implementations:**

1. **Consistent Response Format**: All tools return MCPToolResponse JSON strings
2. **Input Validation**: All inputs validated with Pydantic models
3. **Error Standardization**: All errors use standard ErrorCode enumeration
4. **Resource Structure**: All resources extend MCPResourceData
5. **Type Hints**: All functions have complete type annotations
6. **JSON Serialization**: Use `serialize_for_llm()` for complex data

## Code Style Preferences

### Python Style
- Use type hints for all function parameters and return types
- Use docstrings for all public functions and classes
- Prefer async/await for I/O operations
- **MANDATORY**: Use standardized data types from `src/data_types.py`
- **MANDATORY**: Use logging from `src/logging_config.py`
- Keep functions small and focused (single responsibility)

### File Organization
- Each feature should be self-contained in its own module
- Import statements should be organized: standard library, third-party, local imports
- Use absolute imports from src/ directory
- **Import logging and data types in all feature modules**

### Testing Conventions
- Test files must start with `test_`
- Test functions must start with `test_`
- Use descriptive test names that explain what is being tested
- Mock external dependencies in tests
- **Test both success and error response formats**
- **Test input validation thoroughly**

## Docker Deployment Standards

**CRITICAL: All MCP servers MUST support containerized deployment for production environments.**

### Docker Configuration Requirements

**Multi-Stage Dockerfile Pattern:**
```dockerfile
# Required: Multi-stage build with UV package manager
FROM python:3.12-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.18 /uv /uvx /bin/

# Required: UV environment variables
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Required: Dependency caching
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable

# Required: Production stage with minimal footprint
FROM python:3.12-slim-bookworm AS production
COPY --from=builder /app/.venv /app/.venv
```

### Container Development Commands

**MANDATORY Docker commands for all MCP implementations:**

```bash
# Build optimized production image
docker build --target production -t mcp-server:latest .

# Development with hot reloading
docker-compose --profile development up mcp-server-dev

# Production deployment
docker-compose up -d mcp-server

# SSE transport for web integrations
docker-compose up -d mcp-server-sse

# Containerized testing
docker-compose --profile testing run mcp-server-test

# Container validation
./scripts/docker-run.sh validate
```

### Transport Configuration for Containers

**Stdio Transport (Claude Desktop):**
```bash
# Environment configuration
MCP_HELLO_TRANSPORT_TYPE=stdio
MCP_HELLO_LOG_LEVEL=INFO
```

**SSE Transport (Web Applications):**
```bash
# Port exposure required
docker run -p 8000:8000 -e MCP_HELLO_TRANSPORT_TYPE=sse mcp-server:latest
```

**WebSocket Transport (Real-time):**
```bash
# WebSocket configuration
docker run -p 8001:8001 -e MCP_HELLO_TRANSPORT_TYPE=websocket mcp-server:latest
```

### Container Security Standards

**MANDATORY security requirements:**

1. **Non-root execution**: All containers MUST run as non-root user
2. **Minimal base images**: Use slim-bookworm for production
3. **Resource limits**: Configure memory and CPU limits
4. **Health checks**: Implement proper health monitoring
5. **Secrets management**: Use environment variables or Docker secrets

```dockerfile
# Security requirements
RUN groupadd -r mcp && useradd -r -g mcp mcp
USER mcp

# Health check implementation
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1
```

### Production Deployment Requirements

**Container orchestration support:**
- Docker Compose for local development
- Kubernetes manifests for cloud deployment
- Health checks for load balancer integration
- Resource limits for cluster management

**Monitoring and observability:**
- Structured logging to stdout
- Prometheus metrics endpoints (if applicable)
- Health check endpoints
- Performance monitoring integration

### Docker Helper Script Requirements

**MANDATORY: All MCP features MUST include docker-run.sh script with:**

```bash
./scripts/docker-run.sh build      # Build images
./scripts/docker-run.sh dev        # Development server
./scripts/docker-run.sh prod       # Production server
./scripts/docker-run.sh test       # Run tests
./scripts/docker-run.sh validate   # Validate setup
```

## Important Notes

### What NOT to do
- **NEVER** use pip or conda - only use uv for package management
- **NEVER** commit without running tests first
- **NEVER** build complex solutions when simple ones will work
- **NEVER** add features without corresponding tests
- **NEVER** break the vertical slice architecture

### What TO do
- **ALWAYS** run `uv run pytest` before committing
- **ALWAYS** add tests for new features
- **ALWAYS** use type hints
- **ALWAYS** follow the core principles (KISS, YAGNI, etc.)
- **ALWAYS** use uv commands for package management

## Git Workflow

```bash
# Before committing, always run:
uv run pytest                    # Ensure tests pass
uv run ruff check .             # Check linting (if configured)

# Commit with descriptive messages
git add .
git commit -m "feat: add new MCP tool for X functionality"
```

## Common Tasks

### Adding a New MCP Feature (Complete Workflow)

**Example: Adding a "weather_api" feature**

1. **Create Feature Structure**:
```bash
mkdir -p src/features/weather_api/{api,tools,resources,prompts}
mkdir -p src/features/weather_api/{api/tests,tools/tests,resources/tests,prompts/tests}
touch src/features/weather_api/__init__.py
touch src/features/weather_api/{api,tools,resources,prompts}/__init__.py
touch src/features/weather_api/{api/tests,tools/tests,resources/tests,prompts/tests}/__init__.py
```

2. **Implement Components** (each with co-located test):
   - `src/features/weather_api/api/weather_client.py` + `tests/test_weather_client.py`
   - `src/features/weather_api/tools/get_forecast.py` + `tests/test_get_forecast.py`
   - `src/features/weather_api/resources/current_weather.py` + `tests/test_current_weather.py`
   - `src/features/weather_api/prompts/weather_summary.py` + `tests/test_weather_summary.py`

3. **Validate Structure**:
```bash
# Ensure all tests run
uv run pytest src/features/weather_api/

# Check specific component types
uv run pytest src/features/weather_api/tools/tests/
uv run pytest src/features/weather_api/resources/tests/
```

4. **Register with Main Server** in `src/main_server.py`

### Adding a Single MCP Tool

**Example: Adding a new tool to existing feature**

1. **Create Tool File**: `src/features/github_integration/tools/close_issue.py`
2. **Create Test File**: `src/features/github_integration/tools/tests/test_close_issue.py`
3. **Implement Tool** following FastMCP patterns
4. **Write Comprehensive Tests**
5. **Validate**: `uv run pytest src/features/github_integration/tools/tests/test_close_issue.py`

### Adding Dependencies
```bash
# Add a new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update dependencies
uv sync
```

### Debugging MCP Servers
```bash
# Use MCP Inspector for visual testing
npx @modelcontextprotocol/inspector python src/main_server.py

# Use mcp dev for FastMCP servers
mcp dev src/main_server.py

# Check server logs and errors in terminal output
```

## Environment Setup

### First Time Setup
```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project
git clone <repo-url>
cd mcp_builder
uv sync
uv pip install -e .  # CRITICAL: Install in editable mode for imports
uv run python src/main_server.py
```

### IDE Configuration
- Configure your IDE to use the UV virtual environment
- Set Python interpreter to `.venv/bin/python`
- Enable type checking and linting if available

## Troubleshooting

### Common Issues
- **ImportError**: Make sure to run `uv sync` after pulling changes
- **Module not found**: Check if you're using `uv run` prefix for commands
- **Test failures**: Ensure all dependencies are installed with `uv sync`
- **MCP connection issues**: Verify server syntax and MCP Inspector connectivity

### When Adding New Features
1. Think through the vertical slice architecture
2. Plan the tests first (TDD approach recommended)
3. Implement the minimal viable solution (YAGNI principle)
4. Keep it simple (KISS principle)
5. Ensure it follows dependency inversion where applicable

Remember: This project is about building MCP servers efficiently using specification-driven development through PRPs. Every feature should have a clear purpose and comprehensive tests.