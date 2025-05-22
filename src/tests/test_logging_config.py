"""
Tests for logging_config module.

Tests the standardized logging functionality including setup,
MCPLogger class, performance decorators, and context management.
"""

import logging
from unittest.mock import Mock, patch

import pytest

from src.logging_config import (
    LogLevel,
    LogContext,
    setup_logging,
    MCPLogger,
    log_performance,
    get_mcp_logger,
    setup_mcp_logging,
)


class TestLogLevel:
    """Test LogLevel enumeration."""

    def test_log_levels(self):
        """Test all log levels are defined correctly."""
        assert LogLevel.DEBUG == "DEBUG"
        assert LogLevel.INFO == "INFO"
        assert LogLevel.WARNING == "WARNING"
        assert LogLevel.ERROR == "ERROR"
        assert LogLevel.CRITICAL == "CRITICAL"


class TestLogContext:
    """Test LogContext enumeration."""

    def test_log_contexts(self):
        """Test all log contexts are defined correctly."""
        assert LogContext.TOOL_EXECUTION == "tool_execution"
        assert LogContext.RESOURCE_ACCESS == "resource_access"
        assert LogContext.PROMPT_GENERATION == "prompt_generation"
        assert LogContext.TRANSPORT == "transport"
        assert LogContext.AUTHENTICATION == "authentication"
        assert LogContext.SECURITY == "security"
        assert LogContext.PERFORMANCE == "performance"
        assert LogContext.EXTERNAL_API == "external_api"
        assert LogContext.CONFIGURATION == "configuration"


class TestSetupLogging:
    """Test setup_logging function."""

    def test_setup_standard_logging(self):
        """Test setup with standard Python logging."""
        logger = setup_logging(
            level="INFO", use_structured=False, service_name="test-service"
        )

        assert logger is not None
        assert isinstance(logger, logging.Logger)

    @patch("src.logging_config.STRUCTLOG_AVAILABLE", False)
    def test_setup_fallback_when_structlog_unavailable(self):
        """Test fallback to standard logging when structlog unavailable."""
        logger = setup_logging(
            level="DEBUG",
            use_structured=True,  # Should fallback to standard
            service_name="test-fallback",
        )

        assert logger is not None
        assert isinstance(logger, logging.Logger)

    def test_setup_different_log_levels(self):
        """Test setup with different log levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            logger = setup_logging(level=level, use_structured=False)
            assert logger is not None


class TestMCPLogger:
    """Test MCPLogger class functionality."""

    @pytest.fixture
    def mock_logger(self):
        """Create a mock logger for testing."""
        return Mock()

    @pytest.fixture
    def mcp_logger(self, mock_logger):
        """Create MCPLogger instance with mock logger."""
        return MCPLogger(mock_logger, LogContext.TOOL_EXECUTION)

    def test_mcp_logger_init(self, mock_logger):
        """Test MCPLogger initialization."""
        mcp_logger = MCPLogger(mock_logger, LogContext.TOOL_EXECUTION)
        assert mcp_logger.logger == mock_logger
        assert mcp_logger.context == LogContext.TOOL_EXECUTION

    def test_tool_called(self, mcp_logger):
        """Test tool_called logging method."""
        mcp_logger.tool_called("test_tool", param1="value1", param2=42)

        mcp_logger.logger.info.assert_called_once()
        call_args = mcp_logger.logger.info.call_args
        assert "Tool execution started" in call_args[0]

    def test_tool_completed(self, mcp_logger):
        """Test tool_completed logging method."""
        mcp_logger.tool_completed("test_tool", 150.5, result_size=100)

        mcp_logger.logger.info.assert_called_once()
        call_args = mcp_logger.logger.info.call_args
        assert "Tool execution completed" in call_args[0]

    def test_tool_failed(self, mcp_logger):
        """Test tool_failed logging method."""
        mcp_logger.tool_failed("test_tool", "Test error", 75.2, retry_count=1)

        mcp_logger.logger.error.assert_called_once()
        call_args = mcp_logger.logger.error.call_args
        assert "Tool execution failed" in call_args[0]

    def test_resource_accessed(self, mcp_logger):
        """Test resource_accessed logging method."""
        mcp_logger.resource_accessed("test://resource", cache_hit=True)

        mcp_logger.logger.info.assert_called_once()
        call_args = mcp_logger.logger.info.call_args
        assert "Resource accessed" in call_args[0]

    def test_external_api_call(self, mcp_logger):
        """Test external_api_call logging method."""
        mcp_logger.external_api_call("github", "/api/repos", 200.5, 200, retries=0)

        mcp_logger.logger.info.assert_called_once()
        call_args = mcp_logger.logger.info.call_args
        assert "External API call" in call_args[0]

    def test_security_event(self, mcp_logger):
        """Test security_event logging method."""
        mcp_logger.security_event("auth_failure", user_id="user123", ip="192.168.1.1")

        mcp_logger.logger.warning.assert_called_once()
        call_args = mcp_logger.logger.warning.call_args
        assert "Security event" in call_args[0]

    def test_performance_metric(self, mcp_logger):
        """Test performance_metric logging method."""
        mcp_logger.performance_metric("response_time", 42.5, "ms", endpoint="/test")

        mcp_logger.logger.info.assert_called_once()
        call_args = mcp_logger.logger.info.call_args
        assert "Performance metric" in call_args[0]


class TestLogPerformance:
    """Test log_performance decorator."""

    @pytest.fixture
    def mock_logger(self):
        """Create a mock MCPLogger for testing."""
        logger = Mock()
        logger.tool_called = Mock()
        logger.tool_completed = Mock()
        logger.tool_failed = Mock()
        logger.performance_metric = Mock()
        return logger

    @pytest.mark.asyncio
    async def test_async_function_success(self, mock_logger):
        """Test decorator with successful async function."""

        async def test_async_func(param: str) -> str:
            return f"Result: {param}"

        # Mark as MCP tool
        test_async_func._mcp_tool = True

        # Apply decorator after marking
        decorated_func = log_performance(mock_logger)(test_async_func)

        result = await decorated_func("test")

        assert result == "Result: test"
        mock_logger.tool_called.assert_called_once()
        mock_logger.tool_completed.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_function_failure(self, mock_logger):
        """Test decorator with failing async function."""

        async def test_async_func_fail():
            raise ValueError("Test error")

        # Mark as MCP tool
        test_async_func_fail._mcp_tool = True

        # Apply decorator after marking
        decorated_func = log_performance(mock_logger)(test_async_func_fail)

        with pytest.raises(ValueError, match="Test error"):
            await decorated_func()

        mock_logger.tool_called.assert_called_once()
        mock_logger.tool_failed.assert_called_once()

    def test_sync_function_success(self, mock_logger):
        """Test decorator with successful sync function."""

        @log_performance(mock_logger)
        def test_sync_func(param: str) -> str:
            return f"Result: {param}"

        result = test_sync_func("test")

        assert result == "Result: test"
        mock_logger.performance_metric.assert_called_once()

    def test_sync_function_failure(self, mock_logger):
        """Test decorator with failing sync function."""

        @log_performance(mock_logger)
        def test_sync_func_fail():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            test_sync_func_fail()

        mock_logger.performance_metric.assert_called_once()


class TestGetMCPLogger:
    """Test get_mcp_logger function."""

    def test_get_mcp_logger_defaults(self):
        """Test get_mcp_logger with default parameters."""
        logger = get_mcp_logger()

        assert isinstance(logger, MCPLogger)
        assert logger.context is None

    def test_get_mcp_logger_with_context(self):
        """Test get_mcp_logger with specific context."""
        logger = get_mcp_logger(
            service_name="test-service",
            level="DEBUG",
            context=LogContext.TOOL_EXECUTION,
        )

        assert isinstance(logger, MCPLogger)
        assert logger.context == LogContext.TOOL_EXECUTION

    def test_get_mcp_logger_custom_params(self):
        """Test get_mcp_logger with custom parameters."""
        logger = get_mcp_logger(
            service_name="custom-service", level="WARNING", version="2.0.0"
        )

        assert isinstance(logger, MCPLogger)


class TestSetupMCPLogging:
    """Test setup_mcp_logging function."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration object."""
        config = Mock()
        config.server_name = "test-server"
        config.log_level = "INFO"
        config.version = "1.0.0"
        return config

    def test_setup_mcp_logging(self, mock_config):
        """Test setup_mcp_logging with config object."""
        logger = setup_mcp_logging(mock_config)

        assert isinstance(logger, MCPLogger)

    def test_setup_mcp_logging_missing_version(self, mock_config):
        """Test setup_mcp_logging with missing version attribute."""
        del mock_config.version

        logger = setup_mcp_logging(mock_config)

        assert isinstance(logger, MCPLogger)


class TestIntegration:
    """Integration tests for logging functionality."""

    def test_full_logging_workflow(self):
        """Test complete logging workflow from setup to usage."""
        # Setup logger
        logger = get_mcp_logger(
            service_name="integration-test",
            level="INFO",
            context=LogContext.TOOL_EXECUTION,
        )

        # Test various logging operations
        logger.tool_called("test_tool", param_count=2)
        logger.tool_completed("test_tool", 100.0, success=True)
        logger.performance_metric("memory_usage", 256, "MB")
        logger.security_event("login_attempt", success=True)

        # Should not raise any exceptions
        assert True

    def test_logging_with_real_config(self):
        """Test logging with realistic configuration."""

        # Create a simple config-like object
        class MockConfig:
            server_name = "real-test-server"
            log_level = "DEBUG"
            version = "1.2.3"

        config = MockConfig()
        logger = setup_mcp_logging(config)

        # Test logging operations
        logger.tool_called("real_tool")
        logger.external_api_call("real_api", "/endpoint", 150.0, 200)

        assert isinstance(logger, MCPLogger)


if __name__ == "__main__":
    pytest.main([__file__])
