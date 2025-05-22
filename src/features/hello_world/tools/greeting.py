"""
Simple greeting tool for MCP hello world example.
Demonstrates basic tool implementation with FastMCP patterns.
"""

from typing import Optional


async def say_hello(name: str, greeting: Optional[str] = "Hello") -> str:
    """
    Generate a personalized greeting message.

    This tool demonstrates basic MCP tool functionality by creating
    personalized greetings for users.

    Args:
        name: The name of the person to greet
        greeting: Custom greeting word (defaults to "Hello")

    Returns:
        A formatted greeting message
    """
    if not name.strip():
        raise ValueError("Name cannot be empty")

    # Import config here to avoid circular imports
    from ..config import get_config

    config = get_config()

    return f"{greeting}, {name}! {config.server_welcome_message}"


async def get_server_info() -> str:
    """
    Get information about this MCP server.

    Returns basic information about the server capabilities
    and current status.

    Returns:
        Server information as a formatted string
    """
    # Import config here to avoid circular imports
    from ..config import get_config

    config = get_config()

    info = {
        "server_name": config.server_name,
        "version": config.version,
        "description": config.server_description,
        "capabilities": [
            "greeting",
            "server_info",
            "status_resource",
            "usage_stats_resource",
            "config_resource",
            "formal_greeting_prompt",
            "casual_greeting_prompt",
        ],
        "transport": config.transport_type.value,
    }

    result = "=== MCP Server Information ===\n"
    for key, value in info.items():
        if isinstance(value, list):
            result += f"{key.replace('_', ' ').title()}: {', '.join(value)}\n"
        else:
            result += f"{key.replace('_', ' ').title()}: {value}\n"

    return result
