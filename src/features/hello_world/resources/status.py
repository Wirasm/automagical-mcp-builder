"""
Simple status resource for MCP hello world example.
Demonstrates basic resource implementation with standardized data types and logging.
"""

from datetime import datetime
from typing import List

from src.data_types import MCPResourceData, serialize_for_llm
from src.logging_config import get_mcp_logger, LogContext

# Get logger for resource operations
logger = get_mcp_logger("hello-world-resources", context=LogContext.RESOURCE_ACCESS)


class ServerStatusData(MCPResourceData):
    """Server status resource data model."""

    status: str
    uptime_info: str
    server_name: str
    version: str
    transport_mode: str
    debug_mode: bool
    features_available: List[str]


class UsageStatsData(MCPResourceData):
    """Usage statistics resource data model."""

    total_requests: int
    tools_called: dict
    resources_accessed: dict
    last_activity: datetime


async def get_server_status() -> str:
    """
    Get current server status information.

    This resource provides read-only access to server status data
    that can be consumed by LLMs for understanding server state with
    standardized data format and logging.

    Returns:
        JSON-formatted server status information
    """
    logger.resource_accessed("hello-world://status")

    try:
        # Import config here to avoid circular imports
        from ..config import get_config

        config = get_config()

        # Create standardized status data
        status_data = ServerStatusData(
            status="healthy",
            uptime_info="Server is running normally",
            server_name=config.server_name,
            version=config.version,
            transport_mode=config.transport_type.value,
            debug_mode=config.debug_mode,
            features_available=[
                f"greeting_tool ({'enabled' if config.enable_greeting_tool else 'disabled'})",
                f"server_info_tool ({'enabled' if config.enable_server_info_tool else 'disabled'})",
                f"status_resource ({'enabled' if config.enable_status_resource else 'disabled'})",
                f"usage_stats_resource ({'enabled' if config.enable_usage_stats_resource else 'disabled'})",
                f"formal_greeting_prompt ({'enabled' if config.enable_formal_greeting_prompt else 'disabled'})",
                f"casual_greeting_prompt ({'enabled' if config.enable_casual_greeting_prompt else 'disabled'})",
            ],
            cache_ttl=30,  # 30 seconds cache
            content_type="application/json",
        )

        return serialize_for_llm(status_data)

    except Exception as e:
        logger._log("error", "Failed to get server status", error=str(e))
        # Return minimal error response
        return '{"error": "Failed to retrieve server status", "status": "error"}'


async def get_usage_stats() -> str:
    """
    Get basic usage statistics for the server.

    Returns usage statistics with standardized data format and logging.
    In production, this would track actual usage metrics.

    Returns:
        JSON-formatted usage statistics
    """
    logger.resource_accessed("hello-world://usage-stats")

    try:
        # In a real implementation, this would track actual usage
        # For this example, we'll return mock data with proper structure
        stats_data = UsageStatsData(
            total_requests=0,
            tools_called={"say_hello": 0, "get_server_info": 0},
            resources_accessed={
                "server_status": 0,
                "usage_stats": 1,  # This call itself
            },
            last_activity=datetime.now(),
            cache_ttl=60,  # 1 minute cache
            content_type="application/json",
        )

        return serialize_for_llm(stats_data)

    except Exception as e:
        logger._log("error", "Failed to get usage stats", error=str(e))
        # Return minimal error response
        return '{"error": "Failed to retrieve usage statistics", "total_requests": 0}'
