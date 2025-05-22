Please analyze the MCP server idea: $ARGUMENTS

Create a comprehensive MCP Server Product Requirement Prompt (PRP) by researching and filling out the MCP PRP Base Template.

## Research and Planning Process

Follow these steps to create a complete MCP PRP by copying the MCP template in prps/ant_base_mcp_v1.md and fill out the sections adapted to the users server idea:

### 1. Initial Analysis
Analyze the user's server idea and determine:
- What external system/service/data the MCP server will integrate with
- What problem this MCP server solves for LLM users
- Who the target users are (developers, end users, teams)
- What workflows this enables

### 2. Domain Research
Research the specific domain/service mentioned in the user's server idea:
- Search for API documentation for external services to integrate
- Look for existing MCP servers in similar domains on GitHub
- Research authentication patterns and requirements
- Find rate limits, pricing, and usage constraints
- Identify data formats and transformation needs

### 3. MCP Architecture Planning
Based on your research, plan the MCP server architecture:
- **Transport Selection**: Choose stdio (local), SSE (remote), or WebSocket based on use case
- **Tools Design**: List specific tools (actions) the LLM should be able to call
- **Resources Design**: Identify read-only data sources to expose with URI schemes
- **Prompts Design**: Plan reusable prompt templates for common workflows
- **Authentication**: Determine if OAuth, API keys, or other auth is needed

### 4. Implementation Strategy
Plan the technical implementation approach:
- FastMCP vs low-level MCP SDK decision
- External API client patterns
- Caching and performance strategies  
- Error handling and resilience patterns
- Security considerations

### 5. Testing Strategy
Plan how to validate the MCP server:
- MCP Inspector testing approach
- Claude Desktop integration testing
- Unit and integration test strategies
- Performance and reliability validation

## Template Population

Create a new file called `MCP_SERVER_PRP.md` and fill out the complete MCP Server PRP Base Template with:

1. **Goal Section**: Clear statement of what this MCP server achieves
2. **Why Section**: Business justification and user benefits  
3. **What Section**: Detailed server capabilities and architecture
4. **MCP Architecture Section**: Complete transport, tools, resources, prompts specification
5. **Directory Structure**: Proposed implementation file organization
6. **Implementation Notes**: Technical patterns and considerations specific to this server
7. **Validation Gates**: Specific success criteria and testing requirements
8. **Checkpoints**: Step-by-step implementation and testing milestones

## Key Requirements

Ensure your PRP includes:
- **Specific Tool Signatures**: Exact function names, parameters, and return types
- **Resource URI Schemes**: Complete URI templates with examples
- **External API Integration**: Specific API endpoints, authentication, rate limits
- **Error Handling**: How to handle API failures, network issues, rate limits
- **Security Considerations**: Authentication flows, credential management
- **Performance Requirements**: Caching strategies, response time expectations
- **Client Integration**: How users will configure and use this server

## Example Analysis Framework

For a request like "MCP server for creating infographics with OpenAI image-1 model":

**Domain Research:**
- OpenAI Images API documentation and pricing
- Image generation best practices and prompt engineering
- Template and asset management patterns
- File storage and delivery considerations

**MCP Architecture:**
- Tools: `generate_infographic`, `create_chart`, `apply_template`
- Resources: `templates://{category}`, `examples://{type}`
- Transport: SSE (for team usage) or stdio (for local development)
- Auth: OpenAI API key management

**Implementation Considerations:**
- Image processing and optimization
- Template asset management
- Async generation for long requests
- Error handling for API failures

Remember: Create a planning document, not implementation code. The PRP should provide everything Claude Code needs to successfully build the MCP server, but focus on requirements, architecture, and specification rather than actual Python code.