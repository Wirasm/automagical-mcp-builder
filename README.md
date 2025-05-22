# MCP Builder

A template and builder for creating Model Context Protocol (MCP) servers using vertical slice architecture. This repository provides a complete foundation for building custom MCP servers with Claude Code automation.

## Features

### Hello World MCP Server (Template)

A comprehensive MCP server template demonstrating all core MCP functionality with full configuration support:

- **Tools**: Interactive functions LLMs can call
  - `say_hello_tool` - Generate personalized greetings (configurable)
  - `get_server_info_tool` - Get server information and capabilities

- **Resources**: Read-only data sources
  - `hello-world://status` - Server status and health information
  - `hello-world://usage-stats` - Basic usage statistics
  - `hello-world://config` - Current server configuration (non-sensitive)

- **Prompts**: Reusable prompt templates
  - `formal_greeting` - Generate formal greeting prompts
  - `casual_greeting` - Generate casual greeting prompts

- **Transport Support**: Multiple transport mechanisms
  - **stdio** - For Claude Desktop and local clients
  - **SSE** - For web-based integrations
  - **WebSocket** - For real-time applications

- **Configuration**: Full environment-based configuration
  - Feature toggles for all components
  - Customizable messages and behaviors
  - Transport selection and network settings
  - Debug and logging controls

## How to Use This Template

This template uses Claude Code with automated PRP (Product Requirement Prompt) workflows to build custom MCP servers. Follow these steps to create your own MCP server:

### 1. Clone and Setup

```bash
# Clone this repository
git clone git@github.com:Wirasm/automagical-mcp-builder.git
cd automagical-mcp-builder

# Install dependencies
uv sync
```

### 2. Install Claude Code

Ensure you have Claude Code installed:
- Visit [Claude Code](https://claude.ai/code) for installation instructions
- Verify Claude Code is working in your project directory

### 2.1. Add Library Documentation (Optional)

If your MCP server needs to integrate with specific APIs or libraries, add their documentation:

```bash
# Add library documentation for Claude to reference
touch ai_docs/<library_name>.md
```

Paste the API documentation into the file and save it. Reference it in your PRP description so Claude can use it during generation.

### 3. Generate Your MCP Server PRP

Use Claude Code to create a Product Requirement Prompt for your specific MCP server:

```bash
# Run the MCP initialization command with Claude Code
/command .claude/commands/mcp_init.md $ARGUMENTS
```

Replace `$ARGUMENTS` with a detailed description of what you want to build. The more detail, the better!

Examples:

```bash
# Example 1: GitHub integration
/command .claude/commands/mcp_init.md "Build an MCP server for GitHub integration that allows LLMs to create issues, read repository information, and manage pull requests with OAuth authentication"

# Example 2: Weather service
/command .claude/commands/mcp_init.md "Create a weather MCP server that provides current weather data, forecasts, and weather alerts using OpenWeatherMap API with location-based queries"

# Example 3: Database connector
/command .claude/commands/mcp_init.md "Develop an MCP server for PostgreSQL database operations including querying data, schema inspection, and safe data modifications with connection pooling"
```

### 4. Review the Generated PRP

The MCP initialization command will:
- Research the domain and external APIs you want to integrate
- Analyze existing MCP servers and patterns
- Design the complete MCP architecture (tools, resources, prompts)
- Create a detailed implementation specification
- Generate a comprehensive PRP file in the `prps/` directory

After the command completes:
1. A new PRP file will be created in the `prps/` directory
2. **Manually review the PRP** to ensure it references your project correctly
3. Verify all requirements, APIs, and configurations match your needs
4. Check that authentication patterns and external dependencies are accurate
5. Make any necessary adjustments to the PRP before implementation

### 5. Implement Your MCP Server

Use the implementation command with the path to your PRP:

```bash
# Run the implementation command
/command .claude/commands/implement_prp.md prps/your_generated_prp.md
```

This will automatically:
- Analyze the PRP requirements and dependencies
- Create the complete feature directory structure following vertical slice architecture
- Implement all tools, resources, and prompts specified in the PRP
- Set up configuration and environment handling with proper settings
- Create comprehensive co-located tests for all components
- Configure multi-transport support (stdio, SSE, WebSocket)
- Handle external API integrations and authentication as specified

### 6. Test Your New MCP Server

```bash
# Run tests
uv run pytest src/features/your_feature/ -v

# Start the server
uv run python src/main_server.py

# Test with MCP Inspector
npx @modelcontextprotocol/inspector python src/main_server.py

# Install in Claude Desktop
mcp install src/main_server.py
```

## Troubleshooting

**PRP Generation Issues:**
- If the PRP seems incomplete, provide more detail in your initial description
- Check that external APIs mentioned are publicly documented
- Ensure your requirements are specific enough for implementation

**Implementation Issues:**
- Review the generated PRP for accuracy before running implementation
- Check that all external dependencies are properly specified
- Verify environment variables and configuration match your needs

**Server Issues:**
- Run `uv run pytest` to check all tests pass
- Check logs for configuration or transport errors
- Use debug mode: `MCP_HELLO_DEBUG_MODE=true uv run python src/main_server.py`

**Claude Code Issues:**
- Ensure you're in the correct project directory
- Check that the command files exist in `.claude/commands/`
- Verify Claude Code has access to read the project files

## Quick Start (Hello World Example)

To try the included Hello World example:

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest src/features/hello_world/ -v

# Start the server
uv run python src/main_server.py
```

### Testing with MCP Inspector

```bash
# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Test the server
npx @modelcontextprotocol/inspector python src/main_server.py
```

### Configuration

Copy the example environment file and customize:

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### Integration with Claude Desktop

Add this configuration to your Claude Desktop config:

```json
{
  "mcpServers": {
    "hello-world": {
      "command": "uv",
      "args": ["run", "python", "src/main_server.py"],
      "cwd": "/absolute/path/to/automagical-mcp-builder",
      "env": {
        "MCP_HELLO_TRANSPORT_TYPE": "stdio",
        "MCP_HELLO_DEFAULT_GREETING": "Hello",
        "MCP_HELLO_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Different Transport Examples

**SSE Transport (for web applications):**

```bash
# Set environment variables
export MCP_HELLO_TRANSPORT_TYPE=sse
export MCP_HELLO_HOST=0.0.0.0
export MCP_HELLO_PORT=8000

# Start server
uv run python src/main_server.py

# Server available at http://localhost:8000/sse
```

**WebSocket Transport (for real-time apps):**

```bash
# Set environment variables
export MCP_HELLO_TRANSPORT_TYPE=websocket
export MCP_HELLO_HOST=0.0.0.0
export MCP_HELLO_PORT=8001

# Start server
uv run python src/main_server.py

# Server available at ws://localhost:8001/ws
```

## Architecture

This project follows a vertical slice architecture where each feature is self-contained:

```
src/features/hello_world/
├── tools/          # MCP Tools (LLM-callable functions)
├── resources/      # MCP Resources (read-only data)
├── prompts/        # MCP Prompts (templates)
├── api/            # External API integrations
└── {feature_name}_server.py # Feature's MCP server entry point
```

Each component has co-located tests in `tests/` subdirectories.

## Development

### Adding New Features

1. Create feature directory: `src/features/your_feature/`
2. Implement components following the template in `hello_world/`
3. Create co-located tests for each component
4. Register with main server in `src/main_server.py`

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests for specific feature
uv run pytest src/features/hello_world/

# Run tests for specific component type
uv run pytest src/features/*/tools/tests/
```

### Commands

```bash
# Development workflow
uv sync                           # Install dependencies
uv run python src/main_server.py      # Start server
uv run pytest                    # Run tests
uv run ruff check .              # Lint code

# Testing with MCP tools
npx @modelcontextprotocol/inspector python src/main_server.py
```

## Project Structure

- `src/features/` - Feature implementations (vertical slices)
- `prps/` - Product Requirement Prompts for new features
- `CLAUDE.md` - Project context and development guidelines
- `pyproject.toml` - UV package configuration

For detailed development guidelines, see [CLAUDE.md](./CLAUDE.md).

## Configuration Reference

The server supports extensive configuration through environment variables. All variables are prefixed with `MCP_HELLO_`.

### Server Settings

- `MCP_HELLO_SERVER_NAME` - Server display name (default: "Hello World MCP Server")
- `MCP_HELLO_SERVER_DESCRIPTION` - Server description
- `MCP_HELLO_VERSION` - Server version (default: "1.0.0")

### Transport Settings

- `MCP_HELLO_TRANSPORT_TYPE` - Transport type: stdio, sse, websocket (default: "stdio")
- `MCP_HELLO_HOST` - Host for SSE/WebSocket (default: "localhost")
- `MCP_HELLO_PORT` - Port for SSE/WebSocket (default: "8000")

### Feature Toggles

- `MCP_HELLO_ENABLE_GREETING_TOOL` - Enable/disable greeting tool (default: "true")
- `MCP_HELLO_ENABLE_SERVER_INFO_TOOL` - Enable/disable server info tool (default: "true")
- `MCP_HELLO_ENABLE_STATUS_RESOURCE` - Enable/disable status resource (default: "true")
- `MCP_HELLO_ENABLE_USAGE_STATS_RESOURCE` - Enable/disable usage stats (default: "true")
- `MCP_HELLO_ENABLE_FORMAL_GREETING_PROMPT` - Enable/disable formal prompt (default: "true")
- `MCP_HELLO_ENABLE_CASUAL_GREETING_PROMPT` - Enable/disable casual prompt (default: "true")

### Customization

- `MCP_HELLO_DEFAULT_GREETING` - Default greeting word (default: "Hello")
- `MCP_HELLO_SERVER_WELCOME_MESSAGE` - Welcome message text

### Logging & Debug

- `MCP_HELLO_LOG_LEVEL` - Log level: DEBUG, INFO, WARNING, ERROR (default: "INFO")
- `MCP_HELLO_DEBUG_MODE` - Enable debug output (default: "false")

See `.env.example` for a complete configuration template.