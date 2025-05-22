# Proposed Claude Code Commands for MCP Builder

This directory contains proposed Claude Code commands to improve the MCP Builder development workflow.

## Available Commands

### 1. `fix-imports.md`
Fix Python import management issues in MCP files by:
- Removing manual sys.path manipulation
- Converting to absolute imports from `src/`
- Organizing imports properly

### 2. `setup-project.md`
Setup the MCP Builder project with proper editable installation for import resolution:
- Install UV package manager
- Create virtual environment
- Install project in editable mode
- Verify imports work correctly

### 3. `create-feature.md`
Create a complete MCP feature structure with all required directories and files:
- Full directory structure with api/, tools/, resources/, prompts/
- Base configuration and server files
- Example components with tests

### 4. `add-tool.md`
Add a new MCP tool to an existing feature:
- Create tool implementation with standard imports
- Create co-located test file
- Register tool in feature server

### 5. `add-resource.md`
Add a new MCP resource to an existing feature:
- Create resource with MCPResourceData base class
- Define proper URI scheme
- Create co-located test file

### 6. `validate-feature.md`
Validate that an MCP feature follows all project standards:
- Check directory structure
- Validate naming conventions
- Ensure proper imports and tests
- Verify configuration setup

### 7. `run-tests.md`
Run tests for MCP components with proper UV commands:
- Run all tests or specific subsets
- Use appropriate pytest flags
- Handle common test issues

### 8. `fix-mcp-logging.md`
Fix MCP logging issues that cause JSON-RPC parsing errors:
- Redirect all logging to stderr instead of stdout
- Fix print statements to use stderr
- Ensure MCP protocol compliance

## Critical MCP Server Requirements

### Logging Must Use stderr
**IMPORTANT**: MCP servers communicate via JSON-RPC 2.0 over stdout. Any logging or debug output sent to stdout will break the protocol and cause errors like:
- "Invalid literal value, expected \"2.0\""
- "Unrecognized key(s) in object: 'timestamp', 'level', 'service'..."

**Solution**: All logging has been configured to use stderr:
- `logging.StreamHandler(sys.stderr)` for standard logging
- `structlog.PrintLoggerFactory(file=sys.stderr)` for structured logging
- `print(..., file=sys.stderr)` for any debug prints

## Import Management Solution

The project has been updated to use proper Python package management:

1. **pyproject.toml Configuration**:
   - Uses setuptools package discovery
   - Defines proper package structure
   - Creates editable install entry points

2. **Absolute Imports**:
   - All shared modules use `from src.module import ...`
   - Feature-internal imports use relative imports
   - No manual sys.path manipulation needed

3. **Installation**:
   - Run `uv pip install -e .` to install project
   - This enables proper import resolution
   - All `src/` imports will work correctly

## Usage

These commands are designed to be used with Claude Code:

```bash
# Fix imports in a file
/command fix-imports src/features/weather_api/tools/get_forecast.py

# Create a new feature
/command create-feature github_integration

# Add a tool to a feature
/command add-tool weather_api/get_forecast

# Validate a feature
/command validate-feature weather_api

# Run tests
/command run-tests weather_api -v
```

## Notes

- All commands follow the project's CLAUDE.md guidelines
- Commands enforce vertical slice architecture
- Tests are always co-located with components
- Standardized logging and data types are used throughout