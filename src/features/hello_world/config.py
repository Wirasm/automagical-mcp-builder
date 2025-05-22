"""
Configuration management for Hello World MCP server.
Handles environment variables, transport settings, and server configuration.
"""

import os
from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class TransportType(str, Enum):
    """Available transport types for MCP server."""

    STDIO = "stdio"
    SSE = "sse"
    WEBSOCKET = "websocket"


class HelloWorldConfig(BaseSettings):
    """Configuration for Hello World MCP server."""

    # Server settings
    server_name: str = Field(
        default="Hello World MCP Server", description="Name of the MCP server"
    )
    server_description: str = Field(
        default="A simple example MCP server demonstrating basic functionality",
        description="Description of the MCP server",
    )
    version: str = Field(default="1.0.0", description="Server version")

    # Transport settings
    transport_type: TransportType = Field(
        default=TransportType.STDIO, description="Transport mechanism to use"
    )
    host: str = Field(
        default="localhost", description="Host to bind to for SSE/WebSocket"
    )
    port: int = Field(default=8000, description="Port to bind to for SSE/WebSocket")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format",
    )

    # Feature flags
    enable_greeting_tool: bool = Field(default=True, description="Enable greeting tool")
    enable_server_info_tool: bool = Field(
        default=True, description="Enable server info tool"
    )
    enable_status_resource: bool = Field(
        default=True, description="Enable status resource"
    )
    enable_usage_stats_resource: bool = Field(
        default=True, description="Enable usage stats resource"
    )
    enable_formal_greeting_prompt: bool = Field(
        default=True, description="Enable formal greeting prompt"
    )
    enable_casual_greeting_prompt: bool = Field(
        default=True, description="Enable casual greeting prompt"
    )

    # Custom greeting settings
    default_greeting: str = Field(default="Hello", description="Default greeting word")
    server_welcome_message: str = Field(
        default="Welcome to the MCP Hello World server.",
        description="Welcome message for greetings",
    )

    # Development settings
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    reload_on_change: bool = Field(
        default=False, description="Reload server on file changes (development)"
    )

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "MCP_HELLO_"
        case_sensitive = False


def get_config() -> HelloWorldConfig:
    """Get the server configuration instance."""
    return HelloWorldConfig()


def get_transport_config(config: HelloWorldConfig) -> dict:
    """Get transport-specific configuration."""
    if config.transport_type == TransportType.STDIO:
        return {"type": "stdio"}
    elif config.transport_type == TransportType.SSE:
        return {
            "type": "sse",
            "host": config.host,
            "port": config.port,
            "endpoint": "/sse",
        }
    elif config.transport_type == TransportType.WEBSOCKET:
        return {
            "type": "websocket",
            "host": config.host,
            "port": config.port,
            "endpoint": "/ws",
        }
    else:
        raise ValueError(f"Unsupported transport type: {config.transport_type}")


def print_config_info(config: HelloWorldConfig) -> None:
    """Print current configuration for debugging."""
    print("=== MCP Server Configuration ===")
    print(f"Server: {config.server_name} v{config.version}")
    print(f"Transport: {config.transport_type.value}")

    if config.transport_type in [TransportType.SSE, TransportType.WEBSOCKET]:
        print(f"Address: {config.host}:{config.port}")

    print(f"Debug Mode: {config.debug_mode}")
    print(f"Log Level: {config.log_level}")
    print("================================")
