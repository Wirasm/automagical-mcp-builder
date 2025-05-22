"""
Tests for greeting tools in the Hello World MCP server.
"""

import pytest
from ..greeting import say_hello, get_server_info


class TestSayHello:
    """Test cases for the say_hello tool."""

    @pytest.mark.asyncio
    async def test_say_hello_basic(self):
        """Test basic greeting functionality."""
        result = await say_hello("Alice")
        assert "Hello, Alice!" in result
        assert "Welcome to the MCP Hello World server" in result

    @pytest.mark.asyncio
    async def test_say_hello_custom_greeting(self):
        """Test greeting with custom greeting word."""
        result = await say_hello("Bob", "Hi")
        assert "Hi, Bob!" in result
        assert "Welcome to the MCP Hello World server" in result

    @pytest.mark.asyncio
    async def test_say_hello_empty_name(self):
        """Test that empty name raises appropriate error."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            await say_hello("")

    @pytest.mark.asyncio
    async def test_say_hello_whitespace_name(self):
        """Test that whitespace-only name raises appropriate error."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            await say_hello("   ")


class TestGetServerInfo:
    """Test cases for the get_server_info tool."""

    @pytest.mark.asyncio
    async def test_get_server_info_structure(self):
        """Test that server info returns expected structure."""
        result = await get_server_info()

        # Check for expected content
        assert "Hello World MCP Server" in result
        assert "version" in result.lower()
        assert "capabilities" in result.lower()
        assert "transport" in result.lower()

    @pytest.mark.asyncio
    async def test_get_server_info_capabilities(self):
        """Test that server info includes expected capabilities."""
        result = await get_server_info()

        # Check for expected capabilities
        assert "greeting" in result
        assert "server_info" in result
        assert "status_resource" in result
        assert "greeting_prompt" in result
