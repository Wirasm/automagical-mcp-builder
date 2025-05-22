"""
Simple greeting prompt template for MCP hello world example.
Demonstrates standardized prompt implementation with validation, logging, and data types.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.data_types import MCPPromptTemplate, validate_tool_input
from src.logging_config import get_mcp_logger, LogContext

# Get logger for prompt operations
logger = get_mcp_logger("hello-world-prompts", context=LogContext.PROMPT_GENERATION)


class FormalGreetingInput(BaseModel):
    """Input validation for formal greeting prompt."""

    name: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(default=None, max_length=20)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        return v.strip()

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v and not v.strip():
            raise ValueError("Title cannot be only whitespace")
        # Basic title validation
        if v and len(v.strip()) > 20:
            raise ValueError("Title too long")
        return v.strip() if v else None


class CasualGreetingInput(BaseModel):
    """Input validation for casual greeting prompt."""

    name: str = Field(..., min_length=1, max_length=100)
    context: Optional[str] = Field(default=None, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        return v.strip()

    @field_validator("context")
    @classmethod
    def validate_context(cls, v):
        if v and not v.strip():
            raise ValueError("Context cannot be only whitespace")
        return v.strip() if v else None


async def formal_greeting_prompt(name: str, title: Optional[str] = None) -> str:
    """
    Generate a formal greeting prompt template with validation and logging.

    This prompt provides a template for creating formal greetings
    that can be used by LLMs in various contexts.

    Args:
        name: The name of the person to greet
        title: Optional title (Mr., Ms., Dr., etc.)

    Returns:
        A formatted formal greeting prompt
    """
    # Validate input
    input_data = validate_tool_input(
        FormalGreetingInput, {"name": name, "title": title}
    )

    logger._log(
        "info",
        "Generating formal greeting prompt",
        name=input_data.name,
        title=input_data.title,
    )

    full_name = (
        f"{input_data.title} {input_data.name}" if input_data.title else input_data.name
    )

    prompt_template = MCPPromptTemplate(
        template="""You are tasked with creating a formal greeting for {full_name}.

Please generate a polite and professional greeting that:
1. Addresses {full_name} appropriately
2. Welcomes them warmly
3. Offers assistance if needed
4. Maintains a professional tone

Example format:
"Good [time of day], {full_name}. Welcome to [context]. How may I assist you today?"

Please customize this greeting to be appropriate for the current context and interaction.""",
        parameters={"full_name": full_name},
        description="Formal greeting prompt template for professional contexts",
        category="greeting",
        version="1.0.0",
    )

    result = prompt_template.render(full_name=full_name)

    logger._log(
        "info",
        "Formal greeting prompt generated successfully",
        prompt_length=len(result),
    )

    return result


async def casual_greeting_prompt(name: str, context: Optional[str] = None) -> str:
    """
    Generate a casual greeting prompt template with validation and logging.

    This prompt provides a template for creating casual, friendly greetings
    suitable for informal interactions.

    Args:
        name: The name of the person to greet
        context: Optional context for the greeting (meeting, chat, etc.)

    Returns:
        A formatted casual greeting prompt
    """
    # Validate input
    input_data = validate_tool_input(
        CasualGreetingInput, {"name": name, "context": context}
    )

    logger._log(
        "info",
        "Generating casual greeting prompt",
        name=input_data.name,
        context=input_data.context,
    )

    context_note = f" in this {input_data.context}" if input_data.context else ""

    prompt_template = MCPPromptTemplate(
        template="""You are creating a friendly, casual greeting for {name}.

Please generate a warm and approachable greeting that:
1. Uses {name}'s name naturally
2. Creates a welcoming atmosphere
3. Sets a friendly, relaxed tone
4. Is appropriate for informal interaction{context_note}

Example styles:
- "Hey {name}! Great to see you here!"
- "Hi {name}, welcome! Hope you're doing well."
- "{name}! Good to have you join us."

Feel free to adapt the greeting to match the casual, friendly tone while keeping it genuine and welcoming.""",
        parameters={"name": input_data.name, "context_note": context_note},
        description="Casual greeting prompt template for informal interactions",
        category="greeting",
        version="1.0.0",
    )

    result = prompt_template.render(name=input_data.name, context_note=context_note)

    logger._log(
        "info",
        "Casual greeting prompt generated successfully",
        prompt_length=len(result),
    )

    return result
