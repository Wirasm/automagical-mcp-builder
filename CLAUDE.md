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
uv run python src/main.py
```

## Code Architecture

**IMPORTANT: We follow strict vertical slice architecture where each feature is self-contained with co-located tests. Tests MUST be placed directly next to their related feature components.**

### Complete Project Structure
```
├── ai_docs/                    # AI documentation and context
├── CLAUDE.md                   # This file - project context
├── mcp_builder.egg-info/       # Package metadata (auto-generated)
├── prps/                       # Product Requirement Prompts
│   └── prp_base_template_v1.md # Base MCP PRP template
├── pyproject.toml              # UV package configuration
├── README.md                   # Project documentation
├── src/                        # Source code
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration management
│   ├── server.py               # Main MCP server setup
│   ├── features/               # Feature modules (vertical slices)
│   │   ├── __init__.py
│   │   └── feature_name/       # Individual feature (e.g., github_integration, weather_api, slack_integration)
│   │       ├── __init__.py
│   │       ├── api/            # External API integrations for this feature
│   │       │   ├── __init__.py
│   │       │   ├── feature_api.py      # API client implementation
│   │       │   ├── shared/             # Shared utilities for API
│   │       │   │   ├── __init__.py
│   │       │   │   └── shared.py       # Common API utilities
│   │       │   └── tests/              # API tests
│   │       │       ├── __init__.py
│   │       │       └── test_feature_api.py
│   │       ├── tools/          # MCP Tools (actions LLMs can call)
│   │       │   ├── __init__.py
│   │       │   ├── tool.py             # Tool implementation
│   │       │   └── tests/              # Tool tests (co-located)
│   │       │       ├── __init__.py
│   │       │       └── test_tool.py
│   │       ├── resources/      # MCP Resources (read-only data)
│   │       │   ├── __init__.py
│   │       │   ├── resource.py         # Resource implementation
│   │       │   └── tests/              # Resource tests (co-located)
│   │       │       ├── __init__.py
│   │       │       └── test_resource.py
│   │       └── prompts/        # MCP Prompts (reusable templates)
│   │           ├── __init__.py
│   │           ├── prompt.py           # Prompt implementation
│   │           └── tests/              # Prompt tests (co-located)
│   │               ├── __init__.py
│   │               └── test_prompt.py
│   └── tests/                  # Root-level integration tests
│       ├── __init__.py
│       ├── test_server.py      # Server integration tests
│       ├── test_main.py        # Main application tests
│       └── test_config.py      # Configuration tests
└── uv.lock                     # Dependency lock file (auto-generated)
```

### Vertical Slice Architecture Rules

**CRITICAL: Every component MUST have its test file in the same directory:**

1. **Tools**: `src/features/feature_name/tools/tool.py` → `src/features/feature_name/tools/tests/test_tool.py`
2. **Resources**: `src/features/feature_name/resources/resource.py` → `src/features/feature_name/resources/tests/test_resource.py`  
3. **Prompts**: `src/features/feature_name/prompts/prompt.py` → `src/features/feature_name/prompts/tests/test_prompt.py`
4. **APIs**: `src/features/feature_name/api/feature_api.py` → `src/features/feature_name/api/tests/test_feature_api.py`

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
# Start development
uv sync && uv run python src/main.py

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
uv run mcp dev src/features/{feature_name}/server.py

# Test with MCP Inspector (visual testing)
npx @modelcontextprotocol/inspector python src/features/{feature_name}/server.py

# Install MCP server in Claude Desktop for testing
mcp install src/features/{feature_name}/server.py

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
      "args": ["run", "python", "src/features/{feature_name}/server.py"],
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
2. Test with `uv run mcp dev src/features/{feature}/server.py`
3. Validate with MCP Inspector visual testing
4. Integration test with Claude Desktop configuration
5. Run all co-located tests: `uv run pytest src/features/{feature}/`

### MCP Key Concepts (Quick Reference)
- **Tools**: Functions LLMs can call (like POST endpoints) - implement actions
- **Resources**: Read-only data sources (like GET endpoints) - provide data  
- **Prompts**: Reusable templates for LLM interactions - guide usage
- **Transport**: stdio (local testing), SSE (remote deployment)

## Code Style Preferences

### Python Style
- Use type hints for all function parameters and return types
- Use docstrings for all public functions and classes
- Prefer async/await for I/O operations
- Use Pydantic models for data validation when appropriate
- Keep functions small and focused (single responsibility)

### File Organization
- Each feature should be self-contained in its own module
- Import statements should be organized: standard library, third-party, local imports
- Use absolute imports from src/ directory

### Testing Conventions
- Test files must start with `test_`
- Test functions must start with `test_`
- Use descriptive test names that explain what is being tested
- Mock external dependencies in tests

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

4. **Register with Main Server** in `src/server.py`

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
npx @modelcontextprotocol/inspector python src/server.py

# Use mcp dev for FastMCP servers
mcp dev src/server.py

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
uv run python src/main.py
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