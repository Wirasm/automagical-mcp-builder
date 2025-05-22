"""
Simple greeting tool for MCP hello world example.
Demonstrates standardized tool implementation with validation and logging.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.data_types import validate_tool_input
from src.logging_config import get_mcp_logger, LogContext

# Get logger for tool operations
logger = get_mcp_logger("hello-world-tools", context=LogContext.TOOL_EXECUTION)


class GreetingInput(BaseModel):
    """Input validation for greeting tool."""

    name: str = Field(..., min_length=1, max_length=100)
    greeting: Optional[str] = Field(default="Hello", max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        # Basic name sanitization
        if any(char in v for char in ["<", ">", "&", '"', "'"]):
            raise ValueError("Name contains invalid characters")
        return v.strip()

    @field_validator("greeting")
    @classmethod
    def validate_greeting(cls, v):
        if v and not v.strip():
            raise ValueError("Greeting cannot be only whitespace")
        return v.strip() if v else "Hello"


async def say_hello(name: str, greeting: Optional[str] = "Hello") -> str:
    """
    Generate a personalized greeting message with input validation and logging.

    This tool demonstrates standardized MCP tool functionality by creating
    personalized greetings for users with proper validation.

    Args:
        name: The name of the person to greet
        greeting: Custom greeting word (defaults to "Hello")

    Returns:
        A formatted greeting message
    """
    # Validate input using our standardized validation
    input_data = validate_tool_input(
        GreetingInput, {"name": name, "greeting": greeting}
    )

    logger._log(
        "info",
        "Generating greeting",
        name_length=len(input_data.name),
        greeting_word=input_data.greeting,
    )

    # Import config here to avoid circular imports
    from ..config import get_config

    config = get_config()

    result = (
        f"{input_data.greeting}, {input_data.name}! {config.server_welcome_message}"
    )

    logger._log("info", "Greeting generated successfully", result_length=len(result))

    return result


async def get_server_info() -> str:
    """
    Get information about this MCP server with logging.

    Returns basic information about the server capabilities
    and current status in a structured format.

    Returns:
        Server information as a formatted string
    """
    logger._log("info", "Retrieving server information")

    try:
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

        logger._log(
            "info",
            "Server information retrieved successfully",
            capabilities_count=len(info["capabilities"]),
        )

        return result

    except Exception as e:
        logger._log("error", "Failed to retrieve server information", error=str(e))
        raise
