"""
Simple status resource for MCP hello world example.
Demonstrates basic resource implementation with MCP patterns.
"""

import json
from datetime import datetime


async def get_server_status() -> str:
    """
    Get current server status information.

    This resource provides read-only access to server status data
    that can be consumed by LLMs for understanding server state.

    Returns:
        JSON-formatted server status information
    """
    # Import config here to avoid circular imports
    from ..config import get_config

    config = get_config()

    status_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_info": "Server is running normally",
        "server_name": config.server_name,
        "version": config.version,
        "transport_mode": config.transport_type.value,
        "debug_mode": config.debug_mode,
        "features_available": [
            f"greeting_tool ({'enabled' if config.enable_greeting_tool else 'disabled'})",
            f"server_info_tool ({'enabled' if config.enable_server_info_tool else 'disabled'})",
            f"status_resource ({'enabled' if config.enable_status_resource else 'disabled'})",
            f"usage_stats_resource ({'enabled' if config.enable_usage_stats_resource else 'disabled'})",
            f"formal_greeting_prompt ({'enabled' if config.enable_formal_greeting_prompt else 'disabled'})",
            f"casual_greeting_prompt ({'enabled' if config.enable_casual_greeting_prompt else 'disabled'})",
        ],
    }

    return json.dumps(status_data, indent=2)


async def get_usage_stats() -> str:
    """
    Get basic usage statistics for the server.

    Returns:
        JSON-formatted usage statistics
    """
    # In a real implementation, this would track actual usage
    # For this example, we'll return mock data
    stats_data = {
        "total_requests": 0,
        "tools_called": {"say_hello": 0, "get_server_info": 0},
        "resources_accessed": {
            "server_status": 0,
            "usage_stats": 1,  # This call itself
        },
        "last_activity": datetime.now().isoformat(),
    }

    return json.dumps(stats_data, indent=2)
