"""
Simple greeting prompt template for MCP hello world example.
Demonstrates basic prompt implementation with MCP patterns.
"""

from typing import Optional


async def formal_greeting_prompt(name: str, title: Optional[str] = None) -> str:
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
    if not name.strip():
        raise ValueError("Name cannot be empty")

    full_name = f"{title} {name}" if title else name

    prompt = f"""You are tasked with creating a formal greeting for {full_name}.

Please generate a polite and professional greeting that:
1. Addresses {full_name} appropriately
2. Welcomes them warmly
3. Offers assistance if needed
4. Maintains a professional tone

Example format:
"Good [time of day], {full_name}. Welcome to [context]. How may I assist you today?"

Please customize this greeting to be appropriate for the current context and interaction."""

    return prompt


async def casual_greeting_prompt(name: str, context: Optional[str] = None) -> str:
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
    if not name.strip():
        raise ValueError("Name cannot be empty")

    context_note = f" in this {context}" if context else ""

    prompt = f"""You are creating a friendly, casual greeting for {name}.

Please generate a warm and approachable greeting that:
1. Uses {name}'s name naturally
2. Creates a welcoming atmosphere
3. Sets a friendly, relaxed tone
4. Is appropriate for informal interaction{context_note}

Example styles:
- "Hey {name}! Great to see you here!"
- "Hi {name}, welcome! Hope you're doing well."
- "{name}! Good to have you join us."

Feel free to adapt the greeting to match the casual, friendly tone while keeping it genuine and welcoming."""

    return prompt
