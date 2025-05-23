name: "MCP Server PRP Base Template"
description: |

## Purpose of this Template

This document provides a specialized Product Requirement Prompt (PRP) template for implementing Model Context Protocol (MCP) servers using the Python SDK and FastMCP framework. PRPs serve as comprehensive specifications that provide AI coding assistants with sufficient context to implement MCP servers correctly on the first pass.

The Model Context Protocol (MCP) is an open standard that enables Large Language Models (LLMs) to connect with external data sources, tools, and services in a standardized way. Think of MCP like a USB-C port for AI applications - it provides a universal interface for LLMs to access your data and functionality.

## How to Use This Template

1. Copy this template to create a new MCP Server PRP *** NEVER EDIT THIS TEMPLATE ***
2. Replace the placeholders with your specific MCP server requirements
3. Include sufficient context for each section, referencing existing MCP patterns
4. Be explicit about transport mechanisms, tools, resources, and prompts
5. Include examples from the official MCP documentation
6. Reference security best practices and authentication patterns
7. Fill out all sections, using "N/A" only when a section truly doesn't apply
8. There is example implementation of a hello world server in the hello_world feature. Use this as a reference for when filling out the sections of this template. 
9. Ensure that you remove the hello world routing in src/main_server.py before you implement your MCP server, to avoud it breaking your implementation.
10. We use the official Python SDK for MCP servers. You can find the documentation here: https://github.com/claude-ai/mcp-sdk-python
11. Always keep KISS in mind when filling out this template. Do not overcomplicate things. you can always add more features later.
12. When building an API integration always start by writing a client that can interact with the API. ensure you can conntect to the API and get data from it before you start building the MCP server. (ensure .env variables are set)

---

## Goal

Ensure you include teh following in the instructions for the prp you create after copying this template:
*** REPLACE THE HELLO SERVER AND IMPLEMENTATION WITH THE GOAL OF YOUR MCP SERVER ***

[Concise statement of what this MCP server aims to achieve - what external system/data/functionality it will expose to LLMs]

Example: "Build an MCP server that exposes GitHub repository data and operations to LLMs, enabling natural language queries about code, issues, and pull requests."

## Why

- [Business justification explaining why this MCP server is needed]
- [What LLM workflows this server will enable or enhance]
- [How it integrates with existing AI applications (Claude Desktop, Cursor, etc.)]
- [The value this MCP server brings to users and developers]
- [What problems with current manual data access this solves]

## What

[Detailed explanation of the MCP server to be implemented, including:]

### Core MCP Functionality
- **Transport Mechanism**: [stdio/SSE/WebSocket - specify which and why]
- **Tools**: [List of tools/functions the server will expose to LLMs]
- **Resources**: [Data sources the server will make available as read-only resources]
- **Prompts**: [Pre-built prompt templates for common interactions]
- **Target LLM Clients**: [Claude Desktop, Cursor, MCP Inspector, etc.]

### Server Capabilities
- [Authentication/authorization requirements] (only if applicable)
- [External APIs or services to integrate with] (only if applicable)
- [Data transformation or processing logic needed]
- [Real-time vs. cached data requirements]
- [Error handling and fallback behaviors]

### User Experience
- [How users will discover and use the server's capabilities]
- [Expected interaction patterns with LLMs and clients]
- [Integration requirements with existing workflows] (if applicable)

## MCP Server Architecture

### Transport Implementation
**Primary Transport**: [stdio/SSE/WebSocket]
```
[Specify transport configuration - examples below]

# For stdio (local development/deployment):
- Command: python {feature_name}_server.py
- Communication: Standard input/output streams
- Use case: Local MCP clients, development, Claude Desktop

# For SSE (remote deployment):
- Endpoint: https://your-server.com/sse
- Communication: HTTP + Server-Sent Events
- Use case: Remote clients, web-based integrations

# For WebSocket (advanced real-time):
- Endpoint: wss://your-server.com/ws
- Communication: Bidirectional WebSocket
- Use case: High-frequency real-time interactions
```

### MCP Primitives to Implement

#### Tools (Model-Controlled)
When building tools, always expose docstrings and type hints as these are used by the client and llm to understand the tool's purpose and parameters. read more about this in the MCP documentation.

**CRITICAL: All tools MUST include the MCP Context parameter as a required keyword-only argument (using the `*` syntax) to enable client communication, progress reporting, and advanced features.**

[List each tool the LLM can call - these are like POST endpoints]
```python
# Example tool implementation pattern with full Context usage:
from mcp.server.fastmcp import Context

@mcp.tool()
async def tool_name(param1: str, param2: int, *, ctx: Context) -> str:
    """
    Tool description that the LLM will see
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
        ctx: MCP context for client communication (required)
    
    Returns:
        Description of return value
    """
    # Log to client for visibility
    await ctx.info(f"Processing {param1} with value {param2}")
    await ctx.report_progress(0.1, "Starting processing...")
    
    # Implementation logic here
    try:
        # For long operations, report progress
        await ctx.report_progress(0.5, "Halfway complete...")
        
        result = process_data(param1, param2)
        
        # Log completion
        await ctx.report_progress(1.0, "Processing complete")
        await ctx.info("Successfully processed data")
            
    except Exception as e:
        await ctx.error(f"Processing failed: {str(e)}")
        raise
    
    return result
```

**Tool 1 Name** – Purpose and functionality
- Parameters: [typed parameters with descriptions]
- Returns: [return type and description]
- Side effects: [what this tool does/changes]
- Error conditions: [when this tool might fail]

**Tool 2 Name** – Purpose and functionality
- Parameters: [typed parameters with descriptions]  
- Returns: [return type and description]
- Side effects: [what this tool does/changes]
- Error conditions: [when this tool might fail]

#### Resources (Application-Controlled)
[List read-only data sources - these are like GET endpoints]
```python
# Example resource implementation pattern:
@mcp.resource("resource_uri_template://{param}")
def resource_name(param: str) -> str:
    """
    Resource description
    
    Args:
        param: URI template parameter
        
    Returns:
        Resource content
    """
    # Fetch and return data
    return data
```

**Resource 1 URI**: `scheme://path/{param}`
- Description: [What data this resource provides]
- Parameters: [URI template parameters]
- Content type: [text, JSON, etc.]
- Update frequency: [static, real-time, cached, etc.]

**Resource 2 URI**: `scheme://path/{param}`
- Description: [What data this resource provides]
- Parameters: [URI template parameters]
- Content type: [text, JSON, etc.]
- Update frequency: [static, real-time, cached, etc.]

#### Prompts (User-Controlled)
[List reusable prompt templates for common tasks]
```python
# Example prompt implementation pattern:
@mcp.prompt()
def prompt_name(param1: str) -> str:
    """
    Prompt description
    
    Args:
        param1: Template parameter
        
    Returns:
        Formatted prompt text
    """
    return f"Template with {param1}"
```

**Prompt 1 Name** – Purpose and use case
- Parameters: [template parameters]
- Template: [prompt template structure]
- Use case: [when users would invoke this prompt]

**Prompt 2 Name** – Purpose and use case
- Parameters: [template parameters]
- Template: [prompt template structure]  
- Use case: [when users would invoke this prompt]

## Proposed Directory Structure

**IMPORTANT: Follow the vertical slice architecture defined in CLAUDE.md**

```
src/features/{feature_name}/        # Replace {feature_name} with actual feature
├── __init__.py
├── api/                           # External API integrations
│   ├── __init__.py
│   ├── {service}_client.py        # API client for external service
│   └── tests/
│       ├── __init__.py
│       └── test_{service}_client.py
├── tools/                         # MCP Tools (actions LLM can call)
│   ├── __init__.py
│   ├── {tool_name}.py            # Individual tool implementations
│   └── tests/
│       ├── __init__.py
│       └── test_{tool_name}.py
├── resources/                     # MCP Resources (read-only data)
│   ├── __init__.py
│   ├── {resource_name}.py        # Resource implementations
│   └── tests/
│       ├── __init__.py
│       └── test_{resource_name}.py
├── prompts/                       # MCP Prompts (reusable templates)
│   ├── __init__.py
│   ├── {prompt_name}.py          # Prompt implementations
│   └── tests/
│       ├── __init__.py
│       └── test_{prompt_name}.py
└── {feature_name}_server.py       # Feature's MCP server entry point
```

**Integration Files** (if needed for this specific server):
```
├── config/
│   ├── __init__.py
│   └── {feature}_config.py       # Feature-specific configuration
├── .env.example.{feature}        # Environment variables for this feature
└── claude_desktop_config.json.example  # Client configuration example
```

## Files to Reference

### MCP Official Documentation
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/) (read_only) - Core protocol specification
- [MCP Python SDK Documentation](https://modelcontextprotocol.io/quickstart/server) (read_only) - Official Python SDK 
- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (read_only) - Official example implementation
- [MCP Transport Documentation](https://modelcontextprotocol.io/docs/concepts/transports) (read_only) - Transport mechanisms

### Example MCP Servers
- [Weather Server Example](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples) (read_only) - Official example implementation
- [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) (read_only) - Production MCP server example
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github) (read_only) - API integration patterns

### Security and Best Practices
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tools/debugging) (read_only) - Official security guidance
- [MCP Authentication Patterns](https://developers.cloudflare.com/agents/) (read_only) - OAuth and authentication examples

### Integration Examples
- [Claude Desktop Configuration](https://modelcontextprotocol.io/quickstart/user) (read_only) - Client setup examples
- [MCP Inspector Usage](https://github.com/modelcontextprotocol/inspector) (read_only) - Testing and debugging

## Files to Implement

### Core Server Implementation

1. Start with removing the hello world routing in src/main_server.py before you implement your MCP server, to avoid it breaking your implementation.

2. `{feature_name}_server.py` - Feature's FastMCP server setup

```python
"""
Main MCP server implementation using FastMCP framework.
Initializes server, registers tools/resources/prompts, handles lifecycle.
"""
from fastmcp import FastMCP
from contextlib import asynccontextmanager
from .tools import [tool_modules]
from .resources import [resource_modules]
from .prompts import [prompt_modules]
from .config.settings import get_settings

# Server initialization with lifespan management
@asynccontextmanager
async def app_lifespan(server: FastMCP):
    """Manage server startup and shutdown lifecycle"""
    settings = get_settings()
    # Initialize external connections, databases, etc.
    yield
    # Cleanup on shutdown

mcp = FastMCP(
    name="[SERVER_NAME]",
    description="[SERVER_DESCRIPTION]",
    lifespan=app_lifespan
)

# Register all tools, resources, and prompts
# Implementation follows FastMCP patterns
```

3. `mcp_server/tools/[tool_name].py` - Individual tool implementations

```python
"""
Tool implementation for [TOOL_PURPOSE].
Provides [TOOL_FUNCTIONALITY] to LLMs.
"""
from mcp.server.fastmcp import Context
from typing import [Type annotations]
from src.data_types import success_response, error_response, ErrorCode
from src.logging_config import log_performance

@mcp.tool()
@log_performance(logger)
async def tool_function(
    param1: str,
    param2: int,
    *,
    ctx: Context
) -> str:
    """
    Tool description for LLM consumption.
    
    Args:
        param1: Parameter description
        param2: Parameter description  
        ctx: MCP context for client communication (required)
    
    Returns:
        Standardized JSON response string
    """
    # Use dual logging strategy
    logger.tool_called("tool_function", param1_length=len(param1))
    
    try:
        # Client-visible logging
        await ctx.info(f"Processing {param1}...")
        await ctx.report_progress(0.1, "Initializing...")
        
        # Input validation
        if not param1.strip():
            return error_response(
                ErrorCode.VALIDATION_ERROR,
                "param1 cannot be empty"
            ).to_json_string()
        
        # For long operations, use progress reporting
        await ctx.report_progress(0.5, "Processing data...")
            
        # Implementation logic
        result = await process_data(param1, param2)
        
        # Advanced Context features (when applicable):
        # 1. Read resources: data = await ctx.read_resource("resource://uri")
        # 2. LLM sampling: response = await ctx.sample("Generate text for...")
        # 3. Debug logging: await ctx.debug("Detailed debug info")
        # 4. Warnings: await ctx.warning("Non-critical issue detected")
        
        # Report completion
        await ctx.report_progress(1.0, "Complete")
        await ctx.info("Successfully processed request")
        
        # Return standardized response
        return success_response(
            data=result,
            message=f"Processed {param1} successfully",
            metadata={"param2": param2}
        ).to_json_string()
        
    except Exception as e:
        logger.tool_failed("tool_function", str(e), 0)
        await ctx.error(f"Processing failed: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            f"Failed to process: {str(e)}"
        ).to_json_string()
```

4. `mcp_server/resources/[resource_name].py` - Resource implementations

```python
"""
Resource implementation for [RESOURCE_PURPOSE].
Exposes [DATA_TYPE] as read-only MCP resource.
"""
from fastmcp import Context

async def resource_function(
    param: str,
    ctx: Context
) -> str:
    """
    Resource description.
    
    Args:
        param: URI template parameter
        ctx: MCP context
        
    Returns:
        Resource content
    """
    # Fetch data from external source
    data = fetch_external_data(param)
    
    # Format for LLM consumption
    return format_data(data)
```

### Configuration and Authentication

5. `mcp_server/config/settings.py` - Configuration management

```python
"""
Configuration management for MCP server.
Handles environment variables, secrets, and server settings.
"""
from pydantic import BaseSettings, ConfigDict, field_serializer
from typing import Optional
from datetime import datetime

class Settings(BaseSettings):
    """Server configuration"""
    server_name: str = "[DEFAULT_NAME]"
    server_description: str = "[DEFAULT_DESCRIPTION]"
    
    # External API configurations
    api_key: Optional[str] = None
    api_base_url: str = "[DEFAULT_URL]"
    
    # Transport settings
    transport_type: str = "stdio"  # stdio, sse, websocket
    host: str = "localhost"
    port: int = 8000
    
    # Security settings
    enable_auth: bool = False
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

def get_settings() -> Settings:
    """Get server settings instance"""
    return Settings()
```

6. `mcp_server/auth/oauth_handler.py` - Authentication (if required)

```python
"""
OAuth authentication handler for remote MCP servers.
Implements OAuth 2.1 flow as per MCP specification.
"""
from typing import Optional
import httpx
from .config.settings import get_settings

class OAuthHandler:
    """Handle OAuth flows for MCP server authentication"""
    
    def __init__(self):
        self.settings = get_settings()
        
    async def validate_token(self, token: str) -> bool:
        """Validate OAuth token"""
        # Implementation based on MCP auth spec
        pass
        
    async def refresh_token(self, refresh_token: str) -> Optional[str]:
        """Refresh expired token"""
        # Implementation based on MCP auth spec
        pass
```

### Testing and Validation

7. `tests/test_{feature_name}_server.py` - Server integration tests

```python
"""
Integration tests for MCP server functionality.
Tests server initialization, tool execution, and resource access.
"""
import pytest
from mcp_server.server import mcp
from mcp.client.stdio import stdio_client

@pytest.mark.asyncio
async def test_server_initialization():
    """Test server starts up correctly"""
    # Test server initialization
    assert mcp.name == "[EXPECTED_NAME]"
    
@pytest.mark.asyncio 
async def test_tool_execution():
    """Test tool can be called correctly"""
    # Test tool execution with mock data
    pass

@pytest.mark.asyncio
async def test_resource_access():
    """Test resources return expected data"""
    # Test resource access
    pass
```

## MCP Context Capabilities

**CRITICAL: This section documents the MCP Context features that MUST be leveraged in tool implementations.**

### Context Parameter Usage

All tools MUST include the Context parameter as a required keyword-only argument. The `*` syntax before `ctx: Context` makes it keyword-only, ensuring proper parameter handling by the MCP framework:

1. **Client-Visible Logging**
   - `await ctx.debug()` - Detailed debugging information
   - `await ctx.info()` - General operational messages  
   - `await ctx.warning()` - Important notices
   - `await ctx.error()` - Error conditions

2. **Progress Reporting**
   - `await ctx.report_progress(progress: float, message: str)`
   - Progress should be 0.0 to 1.0
   - Essential for operations > 2 seconds

3. **Resource Access**
   - `await ctx.read_resource(uri: str)` - Read server resources
   - Enables cross-resource data access

4. **LLM Sampling** (when client supports it)
   - `await ctx.sample(prompt: str)` - Request LLM generation
   - Useful for content generation, summarization

### Context Implementation Pattern

```python
@mcp.tool()
async def advanced_tool(
    primary_param: str,
    options: Dict[str, Any] = None,
    *,
    ctx: Context  # Required parameter
) -> str:
    """Tool demonstrating full Context usage."""
    
    # Start with client notification
    await ctx.info(f"Starting processing for {primary_param}")
    await ctx.report_progress(0.0, "Initializing...")
    
    try:
        # Phase 1: Validation
        await ctx.report_progress(0.2, "Validating input...")
        await ctx.debug(f"Input size: {len(primary_param)}")
        
        # Phase 2: Processing
        await ctx.report_progress(0.5, "Processing data...")
        
        # Example: Read additional context from resources
        if options and options.get("use_context"):
            try:
                context_data = await ctx.read_resource("myserver://context/default")
                await ctx.info("Successfully loaded additional context")
            except Exception as e:
                await ctx.warning(f"Could not load context: {str(e)}")
        
        # Phase 3: Advanced features (if applicable)
        if options and options.get("use_llm"):
            try:
                summary = await ctx.sample(f"Summarize this data: {primary_param[:200]}")
                await ctx.info("Generated summary using LLM")
            except Exception as e:
                await ctx.warning(f"LLM sampling unavailable: {str(e)}")
        
        # Complete
        await ctx.report_progress(1.0, "Processing complete")
        await ctx.info("Successfully completed all operations")
            
        return success_response(
            data={"result": "processed"},
            message="Operation completed successfully"
        ).to_json_string()
        
    except Exception as e:
        await ctx.error(f"Operation failed: {str(e)}")
        raise
```

## Implementation Notes

**IMPORTANT: Follow the core principles and patterns established in CLAUDE.md**

### MCP Server Implementation Strategy

**Framework Selection** (Already decided in CLAUDE.md):
- Use FastMCP framework for this server
- Follow our vertical slice architecture pattern
- Implement co-located tests as defined in project standards

**Domain-Specific Implementation Patterns**
[Describe patterns specific to this server's domain/use case]

### Tool Implementation Strategy

**Tool Design for This Server**
[Specific guidance for the tools in this server - what patterns to follow, what external APIs to integrate with, etc.]

**Authentication Requirements for This Server**
[Specify if this server needs OAuth, API keys, or other authentication]

**Error Handling Strategy for This Domain**
[Domain-specific error handling patterns, retry logic, fallback behaviors]

### Logging and Observability Strategy

**CRITICAL: This server MUST implement standardized logging using the MCP Builder logging module.**

**Logging Requirements for This Server:**
```python
# Required imports in all feature modules
from logging_config import setup_mcp_logging, MCPLogger, log_performance, log_context
from data_types import success_response, error_response, ErrorCode

# Setup in {feature_name}_server.py
logger = setup_mcp_logging(config)

# Tool implementation with logging
@mcp.tool()
@log_performance(logger)
async def server_specific_tool(param: str) -> str:
    """Server-specific tool with proper logging."""
    logger.tool_called("server_specific_tool", param_length=len(param))
    
    try:
        # Log external API calls
        with log_context(logger, operation="external_api_call"):
            api_result = await external_api_call(param)
            logger.external_api_call("service_name", "/endpoint", 
                                   duration_ms=150, status_code=200)
        
        return success_response(data=api_result).to_json_string()
        
    except Exception as e:
        logger.tool_failed("server_specific_tool", str(e), 0)
        return error_response(
            ErrorCode.EXTERNAL_API_ERROR,
            "External service unavailable"
        ).to_json_string()
```

**Specific Logging Requirements:**
- **Tool Execution**: Log start, duration, success/failure for all tools
- **External API Integration**: Log all API calls with timing and status codes
- **Authentication Events**: Log login attempts, token validation, authorization failures
- **Performance Metrics**: Track response times, cache hit rates, concurrent users
- **Security Events**: Log suspicious activity, rate limiting triggers, access violations
- **Resource Access**: Track which resources are accessed and how frequently

**Structured Log Context for This Server:**
```python
# Context variables specific to this server's domain
with log_context(logger, 
                user_id="user123",
                organization_id="org456",
                request_id="req789",
                feature_flag="new_feature_enabled"):
    # All operations here include this context
    result = await process_request()
```

### Data Types and Validation Strategy

**CRITICAL: This server MUST use standardized data types from the MCP Builder data types module.**

**Standard Response Implementation:**
```python
from data_types import (
    MCPToolResponse, MCPErrorResponse, MCPResourceData,
    success_response, error_response, ErrorCode,
    validate_tool_input, serialize_for_llm
)

# Example tool with proper data types
@mcp.tool()
async def typed_server_tool(input_data: dict) -> str:
    """Tool with comprehensive input validation and standard responses."""
    try:
        # Define server-specific input model
        class ServerToolInput(BaseModel):
            query: str = Field(..., min_length=1, max_length=1000)
            options: Optional[Dict[str, Any]] = None
            timeout: int = Field(default=30, ge=1, le=300)
            
            @validator('query')
            def validate_query(cls, v):
                # Server-specific validation logic
                if 'forbidden_term' in v.lower():
                    raise ValueError('Query contains forbidden terms')
                return v.strip()
        
        # Validate input
        validated_input = validate_tool_input(ServerToolInput, input_data)
        
        # Process with validated data
        result = await process_query(
            validated_input.query, 
            validated_input.options,
            timeout=validated_input.timeout
        )
        
        # Return standardized success response
        return success_response(
            data=result,
            message=f"Successfully processed query: {validated_input.query[:50]}...",
            metadata={
                "query_length": len(validated_input.query),
                "processing_time": "1.2s",
                "result_count": len(result) if isinstance(result, list) else 1
            }
        ).to_json_string()
        
    except ValueError as e:
        # Input validation error
        return error_response(
            ErrorCode.VALIDATION_ERROR,
            str(e),
            details={"input_data": input_data}
        ).to_json_string()
        
    except TimeoutError:
        # Timeout error
        return error_response(
            ErrorCode.TIMEOUT_ERROR,
            "Request timed out",
            details={"timeout_seconds": validated_input.timeout}
        ).to_json_string()
        
    except Exception as e:
        # Unexpected error
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            f"Unexpected error: {str(e)}"
        ).to_json_string()
```

**Server-Specific Data Models:**
```python
# Define domain-specific data models extending standard base classes

class ServerResourceData(MCPResourceData):
    """Base data model for this server's resources."""
    server_specific_field: str
    validation_status: str
    last_sync: datetime
    
    @field_serializer('last_sync')
    def serialize_last_sync(self, value: datetime) -> str:
        """Serialize last_sync to ISO format."""
        return value.isoformat()

class ServerPromptTemplate(MCPPromptTemplate):
    """Server-specific prompt template structure."""
    domain_category: str
    complexity_level: int = Field(ge=1, le=5)
    required_permissions: List[str] = []

# Usage in resources
@mcp.resource("server://data/{resource_id}")
async def get_server_resource(resource_id: str) -> str:
    """Resource with server-specific data structure."""
    resource_data = ServerResourceData(
        server_specific_field="domain_value",
        validation_status="validated",
        last_sync=datetime.now(),
        cache_ttl=600  # 10 minutes
    )
    return resource_data.model_dump_json(indent=2)
```

**Error Code Strategy for This Server:**
```python
# Define server-specific error codes if needed
class ServerErrorCode(str, Enum):
    """Server-specific error codes extending standard codes."""
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    SERVICE_MAINTENANCE = "SERVICE_MAINTENANCE"
    DATA_CORRUPTION = "DATA_CORRUPTION"
    INTEGRATION_FAILURE = "INTEGRATION_FAILURE"

# Use in error responses
return error_response(
    ServerErrorCode.QUOTA_EXCEEDED,
    "User has exceeded their quota limit",
    details={
        "current_usage": 150,
        "quota_limit": 100,
        "reset_time": "2024-01-01T00:00:00Z"
    }
).to_json_string()
```

**Input Validation Patterns for This Server:**
[Specify the exact input validation requirements for this server's domain - what fields are required, what formats are expected, what business rules must be enforced]

**Response Format Requirements for This Server:**
[Specify any domain-specific response format requirements - special metadata fields, required data structures, LLM consumption patterns]

### Resource Implementation Strategy

**Data Source Integration**
[Specify how to connect to external data sources for this server]

**Caching Strategy for This Server** 
[Whether to cache data, TTL requirements, cache invalidation patterns]

**Data Format and Transformation**
[How to format data from external sources for LLM consumption]

### Performance and Reliability Requirements

**Response Time Requirements**
[Specific latency requirements for this server's use case]

**Rate Limiting Strategy**
[How to handle rate limits from external APIs this server uses]

**Scalability Considerations**
[Whether this server needs to handle multiple concurrent requests]

## Validation Gates

### MCP Protocol Compliance
- [ ] Server implements correct/latest MCP protocol version
- [ ] All tools MUST have proper type annotations and docstrings
- [ ] Resources MUST follow URI template patterns correctly
- [ ] Prompts MUST be properly structured and parameterized
- [ ] Server MUST handle initialization and lifecycle correctly

### Transport Implementation
- [ ] Selected transport (stdio/SSE/WebSocket) MUST work correctly
- [ ] Message serialization/deserialization MUST functions properly
- [ ] Error messages MUST be properly formatted and informative
- [ ] Connection handling MUST be robust with proper cleanup

### Tool Functionality
- [ ] All tools tests must pass running uv run pytest
- [ ] Tools handle invalid inputs gracefully with clear error messages
- [ ] Tools perform expected side effects correctly
- [ ] Tool responses are in the expected format for LLM consumption
- [ ] All tools use standardized MCPToolResponse format
- [ ] All tools implement proper input validation with PydanticV2 models
- [ ] All tools use standard ErrorCode enumeration for errors
- [ ] All tools include Context parameter as required argument (using * syntax)
- [ ] Tools use Context for all client-visible logging and progress reporting
- [ ] Long-running operations (>2s) implement detailed progress reporting via Context
- [ ] Tools use appropriate Context log levels (debug, info, warning, error)
- [ ] Tools demonstrate advanced Context features where applicable (resource reading, LLM sampling)

### Resource Access
- [ ] All resources tests must pass running uv run pytest
- [ ] All resources return data in expected format
- [ ] Parameterized resources handle URI template variables correctly
- [ ] Resource content is appropriate for LLM context consumption
- [ ] Resource access doesn't cause performance issues
- [ ] All resources extend MCPResourceData base class
- [ ] Resource data includes proper metadata and caching information

### Authentication & Security (if applicable)
- [ ] OAuth flow completes successfully for remote servers
- [ ] Token validation works correctly
- [ ] Rate limiting prevents abuse
- [ ] Sensitive data is properly protected
- [ ] Security headers are set appropriately

### Logging and Observability
- [ ] Server uses standardized logging from src/logging_config.py
- [ ] All tools implement @log_performance decorator
- [ ] All tools logging includes start, completion, and error events
- [ ] External API calls are logged with timing and status codes
- [ ] Security events are properly logged and categorized
- [ ] Structured logging context is used for related operations
- [ ] Log levels are appropriate for production deployment
- [ ] Performance metrics are tracked and logged

### Data Types and Validation
- [ ] All tools use MCPToolResponse standard format
- [ ] All inputs are validated using Pydantic models
- [ ] Error responses use standard ErrorCode enumeration
- [ ] Resources extend MCPResourceData base class
- [ ] Custom data models follow project conventions
- [ ] Input validation covers all edge cases and business rules
- [ ] Response serialization uses serialize_for_llm() utility
- [ ] Type hints are complete and accurate throughout

### Client Integration
- [ ] Server can be configured in Claude Desktop successfully (user will test at end of implementation)
- [ ] Server works with other MCP clients (Cursor, etc.) (user will test at end of implementation)
- [ ] Client configuration examples are accurate 

### Pytests
- [ ] All tests pass successfully
- [ ] All tests are co-located with their related feature components

### Ruff
- [ ] All code passes ruff checks
- [ ] All code is formatted according to our project standards

## Implementation Checkpoints/Testing

**IMPORTANT: Follow the testing patterns and commands established in CLAUDE.md**

### 1. Basic Server Setup

**Implementation Steps:**
- Create feature directory following CLAUDE.md vertical slice pattern
- Set up the MCP server following our project standards
- Implement server entry point in `src/features/{feature_name}/{feature_name}_server.py` register it in src/main_server.py

**Testing Approach:**
- Use our project's MCP testing commands from CLAUDE.md
- Verify server follows our project's architectural patterns

**Expected Results:**
- Server initializes using our project structure

**Validation Command:**
```bash
# Use our project's testing pattern
mcp install src/main_server.py
```

### 2. Tool Implementation and Testing

**Implementation Steps:**
- Implement each tool in `src/features/{feature_name}/tools/`
- Create co-located tests following CLAUDE.md patterns
- Follow our type annotation and docstring standards

**Testing Approach:**
- Use our co-located testing strategy
- Run tool-specific tests using our project commands

**Expected Results:**
- All tools work with our testing infrastructure
- Tests follow our project's co-location pattern

**Validation Command:**
```bash
# Test tools using our project pattern
uv run pytest src/features/{feature_name}/tools/tests/
```

### 3. Resource Implementation and Testing

**Validation Command:**
```bash
# Test resources using our project pattern  
uv run pytest src/features/{feature_name}/resources/tests/
```

### 4. Integration Testing with Our Clients


**Validation Command:**
```bash
# Test full feature using our project structure
uv run pytest src/features/{feature_name}/
```

### 5. Production Readiness

**Validation Command:**
```bash
# Run comprehensive tests using our project patterns
uv run pytest src/features/{feature_name}/ -v
```

## Other Considerations

### Performance Optimization
- **Caching**: Implement appropriate caching for expensive operations
- **Rate Limiting**: Protect external APIs from abuse
- **Connection Pooling**: Reuse HTTP connections for external services
- **Async Processing**: Use async/await for I/O bound operations

### Monitoring and Observability
- **Logging**: Structured logging with appropriate log levels
- **Metrics**: Track tool usage, response times, error rates
- **Health Checks**: Implement health endpoints for deployment monitoring
- **Tracing**: Distributed tracing for complex workflows

### Documentation Requirements
- **Update README.md**: remove hello world example and replace with your own
- **API Documentation**: Auto-generated from tool/resource schemas
- **Usage Examples**: in README.md


### Testing Strategy
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test server as a complete system
- **Contract Tests**: Ensure MCP protocol compliance

---

## Claude Code Integration

**IMPORTANT: This PRP is optimized for implementation using Claude Code within our established project patterns.**

### Claude Code Integration with Our Project

This PRP assumes implementation within the MCP Builder project structure defined in CLAUDE.md, which provides:

- **Project Standards**: Core principles (KISS, YAGNI, etc.) and vertical slice architecture
- **UV Package Management**: Established dependency management and workflow commands
- **Testing Patterns**: Co-located testing strategy and validation commands
- **MCP Development Environment**: FastMCP framework preference and testing tools

### Implementation Workflow for This Specific Server

```bash
# Follow our project's development workflow from CLAUDE.md:

# 1. Create feature structure (Claude Code will use our project patterns)
# 2. Implement server following our vertical slice architecture  
# 3. Test using our established MCP testing commands
# 4. Validate with our project's integration patterns
```

### Server-Specific Configuration

**Claude Desktop Configuration for This Server:**
```json
{
  "mcpServers": {
    "{feature_name}": {
      "command": "uv",
      "args": ["run", "python", "src/features/{feature_name}/{feature_name}_server.py"],
      "cwd": "/absolute/path/to/mcp_builder",
      "env": {
        [Server-specific environment variables]
      }
    }
  }
}
```
