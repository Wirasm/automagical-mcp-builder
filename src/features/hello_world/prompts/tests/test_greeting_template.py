"""
Tests for greeting prompt templates in the Hello World MCP server.
"""

import pytest
from ..greeting_template import formal_greeting_prompt, casual_greeting_prompt


class TestFormalGreetingPrompt:
    """Test cases for the formal_greeting_prompt."""

    @pytest.mark.asyncio
    async def test_formal_greeting_basic(self):
        """Test basic formal greeting prompt generation."""
        result = await formal_greeting_prompt("Alice")

        # Should contain the name
        assert "Alice" in result
        # Should be a formal greeting prompt
        assert "formal greeting" in result.lower()
        assert "professional" in result.lower()
        # Should include instructions
        assert "generate" in result.lower()
        assert "greeting" in result.lower()

    @pytest.mark.asyncio
    async def test_formal_greeting_with_title(self):
        """Test formal greeting prompt with title."""
        result = await formal_greeting_prompt("Smith", "Dr.")

        # Should contain both title and name
        assert "Dr. Smith" in result
        # Should be formal
        assert "formal greeting" in result.lower()

    @pytest.mark.asyncio
    async def test_formal_greeting_empty_name(self):
        """Test that empty name raises appropriate error."""
        with pytest.raises(ValueError, match=r"Input validation failed"):
            await formal_greeting_prompt("")

    @pytest.mark.asyncio
    async def test_formal_greeting_whitespace_name(self):
        """Test that whitespace-only name raises appropriate error."""
        with pytest.raises(
            ValueError, match=r"Name cannot be empty or only whitespace"
        ):
            await formal_greeting_prompt("   ")


class TestCasualGreetingPrompt:
    """Test cases for the casual_greeting_prompt."""

    @pytest.mark.asyncio
    async def test_casual_greeting_basic(self):
        """Test basic casual greeting prompt generation."""
        result = await casual_greeting_prompt("Bob")

        # Should contain the name
        assert "Bob" in result
        # Should be a casual greeting prompt
        assert "casual" in result.lower()
        assert "friendly" in result.lower()
        # Should include instructions
        assert "generate" in result.lower()
        assert "greeting" in result.lower()

    @pytest.mark.asyncio
    async def test_casual_greeting_with_context(self):
        """Test casual greeting prompt with context."""
        result = await casual_greeting_prompt("Charlie", "meeting")

        # Should contain name and context
        assert "Charlie" in result
        assert "meeting" in result
        # Should be casual
        assert "casual" in result.lower()

    @pytest.mark.asyncio
    async def test_casual_greeting_empty_name(self):
        """Test that empty name raises appropriate error."""
        with pytest.raises(ValueError, match=r"Input validation failed"):
            await casual_greeting_prompt("")

    @pytest.mark.asyncio
    async def test_casual_greeting_whitespace_name(self):
        """Test that whitespace-only name raises appropriate error."""
        with pytest.raises(
            ValueError, match=r"Name cannot be empty or only whitespace"
        ):
            await casual_greeting_prompt("   ")

    @pytest.mark.asyncio
    async def test_casual_greeting_examples(self):
        """Test that casual greeting includes helpful examples."""
        result = await casual_greeting_prompt("Dana")

        # Should include example patterns
        assert "example" in result.lower()
        # Should show casual greeting patterns
        assert "Hey" in result or "Hi" in result
