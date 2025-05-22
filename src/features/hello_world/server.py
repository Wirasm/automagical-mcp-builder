#!/usr/bin/env python3
"""
Hello World MCP Server - Basic template demonstrating MCP functionality.

This server provides a simple example of MCP server implementation with:
- Basic tools (greeting, server info)
- Simple resources (status, usage stats)
- Prompt templates (formal/casual greetings)
- Support for multiple transports (stdio, SSE, WebSocket)
"""

import logging
import sys
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Import our feature components
from .config import (
    HelloWorldConfig,
    TransportType,
    get_config,
    get_transport_config,
    print_config_info,
)
from .prompts.greeting_template import casual_greeting_prompt, formal_greeting_prompt
from .resources.status import get_server_status, get_usage_stats
from .tools.greeting import get_server_info, say_hello

# Get configuration
config = get_config()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level.upper()), format=config.log_format
)
logger = logging.getLogger("hello-world-mcp")

# Create the FastMCP server instance
mcp = FastMCP(config.server_name)


@mcp.tool()
async def say_hello_tool(name: str, greeting: Optional[str] = None) -> str:
    """
    Generate a personalized greeting message.

    This tool demonstrates basic MCP tool functionality by creating
    personalized greetings for users.

    Args:
        name: The name of the person to greet
        greeting: Custom greeting word (defaults to server configured greeting)

    Returns:
        A formatted greeting message
    """
    if not config.enable_greeting_tool:
        return "Greeting tool is currently disabled."

    effective_greeting = greeting or config.default_greeting
    return await say_hello(name, effective_greeting)


@mcp.tool()
async def get_server_info_tool() -> str:
    """
    Get information about this MCP server.

    Returns basic information about the server capabilities
    and current status.

    Returns:
        Server information as a formatted string
    """
    if not config.enable_server_info_tool:
        return "Server info tool is currently disabled."

    return await get_server_info()


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

    # Get transport configuration
    transport_config = get_transport_config(config)

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
