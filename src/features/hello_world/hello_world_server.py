#!/usr/bin/env python3
"""
Hello World MCP Server - Basic template demonstrating MCP functionality.

This server provides a simple example of MCP server implementation with:
- Basic tools (greeting, server info)
- Simple resources (status, usage stats)
- Prompt templates (formal/casual greetings)
- Support for multiple transports (stdio, SSE, WebSocket)
"""

import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP, Context

# Add the project root to Python path for src imports
# This is needed when running via Claude Desktop or other external processes
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import standardized logging and data types
from src.logging_config import setup_mcp_logging, log_performance  # noqa: E402
from src.data_types import success_response, error_response, ErrorCode  # noqa: E402

# Import our feature components
from .config import (
    TransportType,
    get_config,
    print_config_info,
)
from .prompts.greeting_template import casual_greeting_prompt, formal_greeting_prompt
from .resources.status import get_server_status, get_usage_stats
from .tools.greeting import get_server_info, say_hello

# Get configuration
config = get_config()

# Setup standardized logging
logger = setup_mcp_logging(config)

# Create the FastMCP server instance
mcp = FastMCP(config.server_name)

# Note: All tools below use the * syntax before ctx: Context to make it a required
# keyword-only argument. This ensures proper parameter handling by the MCP framework
# and enables rich client communication features.


@mcp.tool()
@log_performance(logger)
async def say_hello_tool(name: str, greeting: Optional[str] = None, *, ctx: Context) -> str:
    """
    Generate a personalized greeting message.

    This tool demonstrates basic MCP tool functionality by creating
    personalized greetings for users with standardized logging and validation.

    Args:
        name: The name of the person to greet
        greeting: Custom greeting word (defaults to server configured greeting)
        ctx: MCP context for client communication (required)

    Returns:
        A standardized JSON response with greeting message
    """
    # Use MCP context logging for client visibility
    await ctx.info(f"Generating greeting for {name}")
    
    logger.tool_called("say_hello_tool", name_length=len(name) if name else 0)

    try:
        # Check if tool is enabled
        if not config.enable_greeting_tool:
            return error_response(
                ErrorCode.CONFIGURATION_ERROR, "Greeting tool is currently disabled"
            ).to_json_string()

        # Input validation
        if not name or not name.strip():
            return error_response(
                ErrorCode.VALIDATION_ERROR,
                "Name parameter is required and cannot be empty",
            ).to_json_string()

        # Process request
        effective_greeting = greeting or config.default_greeting
        
        # Report progress for demonstration (useful for longer operations)
        await ctx.report_progress(0.5, "Processing greeting...")
        
        result = await say_hello(name.strip(), effective_greeting)
        
        # Log completion to client
        await ctx.info(f"Successfully generated greeting for {name}")

        return success_response(
            data={"greeting": result},
            message=f"Generated greeting for {name}",
            metadata={
                "greeting_word": effective_greeting,
                "name_length": len(name.strip()),
                "server_version": config.version,
            },
        ).to_json_string()

    except Exception as e:
        logger.tool_failed("say_hello_tool", str(e), 0)
        return error_response(
            ErrorCode.INTERNAL_ERROR, f"Failed to generate greeting: {str(e)}"
        ).to_json_string()


@mcp.tool()
@log_performance(logger)
async def get_server_info_tool(*, ctx: Context) -> str:
    """
    Get information about this MCP server.

    Returns basic information about the server capabilities
    and current status with standardized response format.

    Args:
        ctx: MCP context for client communication (required)

    Returns:
        JSON-formatted server information response
    """
    # Use MCP context logging for client visibility
    await ctx.info("Retrieving server information...")
    
    logger.tool_called("get_server_info_tool")

    try:
        # Check if tool is enabled
        if not config.enable_server_info_tool:
            return error_response(
                ErrorCode.CONFIGURATION_ERROR, "Server info tool is currently disabled"
            ).to_json_string()

        # Get server information
        server_info = await get_server_info()
        
        # Log completion to client
        await ctx.info("Server information retrieved successfully")

        return success_response(
            data={"server_info": server_info},
            message="Server information retrieved successfully",
            metadata={
                "request_timestamp": str(config.version),
                "transport_type": config.transport_type.value,
            },
        ).to_json_string()

    except Exception as e:
        logger.tool_failed("get_server_info_tool", str(e), 0)
        return error_response(
            ErrorCode.INTERNAL_ERROR, f"Failed to retrieve server information: {str(e)}"
        ).to_json_string()


@mcp.resource("hello-world://status")
async def get_status_resource() -> str:
    """
    Get current server status information.

    This resource provides read-only access to server status data
    that can be consumed by LLMs for understanding server state.

    Returns:
        JSON-formatted server status information
    """
    if not config.enable_status_resource:
        return '{"error": "Status resource is currently disabled."}'

    return await get_server_status()


@mcp.resource("hello-world://usage-stats")
async def get_usage_stats_resource() -> str:
    """
    Get basic usage statistics for the server.

    Returns:
        JSON-formatted usage statistics
    """
    if not config.enable_usage_stats_resource:
        return '{"error": "Usage stats resource is currently disabled."}'

    return await get_usage_stats()


@mcp.resource("hello-world://config")
async def get_config_resource() -> str:
    """
    Get current server configuration (non-sensitive).

    Returns:
        JSON-formatted configuration information
    """
    import json

    safe_config = {
        "server_name": config.server_name,
        "server_description": config.server_description,
        "version": config.version,
        "transport_type": config.transport_type.value,
        "features_enabled": {
            "greeting_tool": config.enable_greeting_tool,
            "server_info_tool": config.enable_server_info_tool,
            "status_resource": config.enable_status_resource,
            "usage_stats_resource": config.enable_usage_stats_resource,
            "formal_greeting_prompt": config.enable_formal_greeting_prompt,
            "casual_greeting_prompt": config.enable_casual_greeting_prompt,
        },
        "customization": {
            "default_greeting": config.default_greeting,
            "welcome_message": config.server_welcome_message,
        },
    }

    return json.dumps(safe_config, indent=2)


@mcp.tool()
@log_performance(logger)
async def process_greeting_with_context(name: str, style: str = "formal", *, ctx: Context) -> str:
    """
    Advanced greeting processor demonstrating full MCP Context capabilities.
    
    This tool showcases all MCP Context features including logging, progress
    reporting, resource reading, and LLM sampling.
    
    Args:
        name: The name of the person to greet
        style: Greeting style - "formal", "casual", or "creative"
        ctx: MCP context for advanced client communication (required)
        
    Returns:
        A contextually-aware greeting message
    """
    logger.tool_called("process_greeting_with_context", style=style)
    
    try:
        # Step 1: Log start and validate input
        await ctx.info(f"Starting advanced greeting generation for {name} with {style} style")
        await ctx.report_progress(0.1, "Validating input...")
        
        if not name or not name.strip():
            return error_response(
                ErrorCode.VALIDATION_ERROR,
                "Name parameter is required"
            ).to_json_string()
            
        # Step 2: Check if we can read any user preferences (demonstration)
        if style == "creative":
            await ctx.report_progress(0.3, "Checking for creative inspiration...")
            try:
                # Example: Try to read a resource for context
                # In a real implementation, this might read user preferences
                await ctx.debug(f"Attempting to generate creative greeting for {name}")
                
                # Step 3: Use LLM sampling for creative greetings
                await ctx.report_progress(0.5, "Generating creative greeting with LLM...")
                
                prompt = f"Generate a creative, unique greeting for someone named {name}. Make it memorable and fun!"
                
                try:
                    llm_result = await ctx.sample(prompt)
                    if llm_result and hasattr(llm_result, 'text'):
                        await ctx.info("Successfully generated creative greeting using LLM")
                        return success_response(
                            data={"greeting": llm_result.text},
                            message="Generated creative greeting with LLM assistance",
                            metadata={"style": "creative", "llm_generated": True}
                        ).to_json_string()
                except Exception as llm_error:
                    await ctx.warning(f"LLM sampling failed, falling back to template: {str(llm_error)}")
                    
            except Exception as e:
                await ctx.warning(f"Could not access advanced features: {str(e)}")
        
        # Step 4: Generate greeting based on style
        await ctx.report_progress(0.7, f"Generating {style} greeting...")
            
        if style == "formal":
            greeting = f"Good day, {name}. It is a pleasure to make your acquaintance."
        elif style == "casual":
            greeting = f"Hey {name}! Great to see you!"
        else:
            greeting = f"Hello {name}! Welcome to our MCP server."
            
        # Step 5: Log completion
        await ctx.report_progress(1.0, "Greeting generation complete")
        await ctx.info(f"Successfully generated {style} greeting")
            
        return success_response(
            data={"greeting": greeting},
            message=f"Generated {style} greeting for {name}",
            metadata={
                "style": style,
                "name_length": len(name),
                "llm_generated": False
            }
        ).to_json_string()
        
    except Exception as e:
        logger.tool_failed("process_greeting_with_context", str(e), 0)
        await ctx.error(f"Failed to generate greeting: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            f"Failed to process greeting: {str(e)}"
        ).to_json_string()


@mcp.prompt()
async def formal_greeting(name: str, title: Optional[str] = None) -> str:
    """
    Generate a formal greeting prompt template.

    This prompt provides a template for creating formal greetings
    that can be used by LLMs in various contexts.

    Args:
        name: The name of the person to greet
        title: Optional title (Mr., Ms., Dr., etc.)

    Returns:
        A formatted formal greeting prompt
    """
    if not config.enable_formal_greeting_prompt:
        return "Formal greeting prompt is currently disabled."

    return await formal_greeting_prompt(name, title)


@mcp.prompt()
async def casual_greeting(name: str, context: Optional[str] = None) -> str:
    """
    Generate a casual greeting prompt template.

    This prompt provides a template for creating casual, friendly greetings
    suitable for informal interactions.

    Args:
        name: The name of the person to greet
        context: Optional context for the greeting (meeting, chat, etc.)

    Returns:
        A formatted casual greeting prompt
    """
    if not config.enable_casual_greeting_prompt:
        return "Casual greeting prompt is currently disabled."

    return await casual_greeting_prompt(name, context)


def main():
    """Main entry point for the Hello World MCP server."""
    # Print configuration info if in debug mode
    if config.debug_mode:
        print_config_info(config)

    logger.info(f"Starting {config.server_name} v{config.version}...")
    logger.info(f"Transport: {config.transport_type.value}")

    if config.transport_type == TransportType.STDIO:
        logger.info("Using stdio transport")
        mcp.run()
    elif config.transport_type == TransportType.SSE:
        logger.info(f"Using SSE transport on {config.host}:{config.port}")
        mcp.run(transport="sse", host=config.host, port=config.port)
    elif config.transport_type == TransportType.WEBSOCKET:
        logger.info(f"Using WebSocket transport on {config.host}:{config.port}")
        mcp.run(transport="ws", host=config.host, port=config.port)
    else:
        logger.error(f"Unsupported transport type: {config.transport_type}")
        sys.exit(1)


if __name__ == "__main__":
    main()
