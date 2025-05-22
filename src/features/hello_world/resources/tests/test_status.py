"""
Tests for status resources in the Hello World MCP server.
"""

import json
import pytest
from datetime import datetime
from ..status import get_server_status, get_usage_stats


class TestGetServerStatus:
    """Test cases for the get_server_status resource."""

    @pytest.mark.asyncio
    async def test_get_server_status_format(self):
        """Test that server status returns valid JSON."""
        result = await get_server_status()

        # Should be valid JSON
        status_data = json.loads(result)
        assert isinstance(status_data, dict)

    @pytest.mark.asyncio
    async def test_get_server_status_content(self):
        """Test that server status contains expected fields."""
        result = await get_server_status()
        status_data = json.loads(result)

        # Check required fields (new standardized format)
        assert "status" in status_data
        assert "last_updated" in status_data  # Changed from "timestamp"
        assert "uptime_info" in status_data
        assert "features_available" in status_data
        assert "version" in status_data
        assert "transport_mode" in status_data

        # Check metadata fields from MCPResourceData
        assert "cache_ttl" in status_data
        assert "content_type" in status_data

        # Check values
        assert status_data["status"] == "healthy"
        assert status_data["version"] == "1.0.0"
        assert status_data["transport_mode"] == "stdio"
        assert isinstance(status_data["features_available"], list)
        assert status_data["content_type"] == "application/json"

    @pytest.mark.asyncio
    async def test_get_server_status_timestamp(self):
        """Test that server status includes valid timestamp."""
        result = await get_server_status()
        status_data = json.loads(result)

        # Should be able to parse timestamp (now called last_updated)
        timestamp_str = status_data["last_updated"]
        timestamp = datetime.fromisoformat(timestamp_str)
        assert isinstance(timestamp, datetime)


class TestGetUsageStats:
    """Test cases for the get_usage_stats resource."""

    @pytest.mark.asyncio
    async def test_get_usage_stats_format(self):
        """Test that usage stats returns valid JSON."""
        result = await get_usage_stats()

        # Should be valid JSON
        stats_data = json.loads(result)
        assert isinstance(stats_data, dict)

    @pytest.mark.asyncio
    async def test_get_usage_stats_content(self):
        """Test that usage stats contains expected fields."""
        result = await get_usage_stats()
        stats_data = json.loads(result)

        # Check required fields
        assert "total_requests" in stats_data
        assert "tools_called" in stats_data
        assert "resources_accessed" in stats_data
        assert "last_activity" in stats_data

        # Check structure
        assert isinstance(stats_data["tools_called"], dict)
        assert isinstance(stats_data["resources_accessed"], dict)
        assert "say_hello" in stats_data["tools_called"]
        assert "get_server_info" in stats_data["tools_called"]

    @pytest.mark.asyncio
    async def test_get_usage_stats_self_increment(self):
        """Test that usage stats increments itself."""
        result = await get_usage_stats()
        stats_data = json.loads(result)

        # Should show this call incremented usage stats
        assert stats_data["resources_accessed"]["usage_stats"] == 1
