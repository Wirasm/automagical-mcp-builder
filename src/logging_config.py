"""
MCP Builder Logging Configuration Module.

Provides standardized logging patterns for all MCP servers built with this template.
Supports structured logging, performance tracking, and security auditing.
"""

import logging
import sys
import time
from contextlib import contextmanager
from functools import wraps
from typing import Optional, Union

try:
    import structlog

    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False

from enum import Enum


class LogLevel(str, Enum):
    """Standard log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogContext(str, Enum):
    """Standard log contexts for MCP operations."""

    TOOL_EXECUTION = "tool_execution"
    RESOURCE_ACCESS = "resource_access"
    PROMPT_GENERATION = "prompt_generation"
    TRANSPORT = "transport"
    AUTHENTICATION = "authentication"
    SECURITY = "security"
    PERFORMANCE = "performance"
    EXTERNAL_API = "external_api"
    CONFIGURATION = "configuration"


def setup_logging(
    level: str = "INFO",
    use_structured: bool = True,
    service_name: str = "mcp-server",
    version: str = "1.0.0",
) -> logging.Logger:
    """
    Setup standardized logging for MCP servers.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_structured: Use structured logging if available
        service_name: Name of the MCP server for log identification
        version: Version of the MCP server

    Returns:
        Configured logger instance
    """
    if use_structured and STRUCTLOG_AVAILABLE:
        return _setup_structured_logging(level, service_name, version)
    else:
        return _setup_standard_logging(level, service_name)


def _setup_structured_logging(
    level: str, service_name: str, version: str
) -> logging.Logger:
    """Setup structured logging with structlog."""
    import io
    
    # CRITICAL: Configure structlog to use stderr for MCP servers
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            _add_service_info(service_name, version),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def _setup_standard_logging(level: str, service_name: str) -> logging.Logger:
    """Setup standard Python logging with JSON-like format."""
    logger = logging.getLogger(service_name)

    if not logger.handlers:
        # CRITICAL: Use stderr for MCP servers to avoid interfering with JSON-RPC protocol
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"service": "' + service_name + '", "message": "%(message)s", '
            '"module": "%(name)s", "function": "%(funcName)s", "line": %(lineno)d}'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, level.upper()))

    return logger


def _add_service_info(service_name: str, version: str):
    """Add service information to structured logs."""

    def processor(logger, method_name, event_dict):
        event_dict["service"] = service_name
        event_dict["version"] = version
        return event_dict

    return processor


class MCPLogger:
    """
    Enhanced logger wrapper for MCP operations with context management.

    Provides standardized logging patterns for MCP tools, resources, and prompts.
    """

    def __init__(self, logger: logging.Logger, context: Optional[LogContext] = None):
        self.logger = logger
        self.context = context

    def tool_called(self, tool_name: str, **kwargs) -> None:
        """Log tool execution start."""
        self._log(
            "info",
            "Tool execution started",
            context=LogContext.TOOL_EXECUTION,
            tool_name=tool_name,
            **kwargs,
        )

    def tool_completed(self, tool_name: str, duration_ms: float, **kwargs) -> None:
        """Log successful tool completion."""
        log_data = {
            "context": LogContext.TOOL_EXECUTION,
            "tool_name": tool_name,
            "duration_ms": duration_ms,
            "success": True,
        }
        log_data.update(kwargs)
        self._log("info", "Tool execution completed", **log_data)

    def tool_failed(
        self, tool_name: str, error: str, duration_ms: float, **kwargs
    ) -> None:
        """Log tool execution failure."""
        log_data = {
            "context": LogContext.TOOL_EXECUTION,
            "tool_name": tool_name,
            "error": error,
            "duration_ms": duration_ms,
            "success": False,
        }
        log_data.update(kwargs)
        self._log("error", "Tool execution failed", **log_data)

    def resource_accessed(self, resource_uri: str, **kwargs) -> None:
        """Log resource access."""
        self._log(
            "info",
            "Resource accessed",
            context=LogContext.RESOURCE_ACCESS,
            resource_uri=resource_uri,
            **kwargs,
        )

    def external_api_call(
        self,
        api_name: str,
        endpoint: str,
        duration_ms: float,
        status_code: int,
        **kwargs,
    ) -> None:
        """Log external API calls."""
        self._log(
            "info",
            "External API call",
            context=LogContext.EXTERNAL_API,
            api_name=api_name,
            endpoint=endpoint,
            duration_ms=duration_ms,
            status_code=status_code,
            **kwargs,
        )

    def security_event(self, event_type: str, **kwargs) -> None:
        """Log security-related events."""
        self._log(
            "warning",
            "Security event",
            context=LogContext.SECURITY,
            event_type=event_type,
            **kwargs,
        )

    def performance_metric(
        self, metric_name: str, value: Union[int, float], unit: str, **kwargs
    ) -> None:
        """Log performance metrics."""
        self._log(
            "info",
            "Performance metric",
            context=LogContext.PERFORMANCE,
            metric_name=metric_name,
            value=value,
            unit=unit,
            **kwargs,
        )

    def _log(self, level: str, message: str, **kwargs) -> None:
        """Internal logging method."""
        if STRUCTLOG_AVAILABLE and hasattr(self.logger, level):
            getattr(self.logger, level)(message, **kwargs)
        else:
            # Fallback for standard logging
            extra_info = " ".join(f"{k}={v}" for k, v in kwargs.items())
            full_message = f"{message} {extra_info}" if extra_info else message
            getattr(self.logger, level)(full_message)


def log_performance(logger: MCPLogger):
    """
    Decorator to automatically log tool/function performance.

    Args:
        logger: MCPLogger instance

    Returns:
        Decorator function
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            func_name = func.__name__

            try:
                # Log start if it's a tool
                is_mcp_tool = hasattr(func, "_mcp_tool")
                if is_mcp_tool:
                    logger.tool_called(
                        func_name, args_count=len(args), kwargs_count=len(kwargs)
                    )

                result = await func(*args, **kwargs)
                duration_ms = round((time.time() - start_time) * 1000, 2)

                # Log completion
                if is_mcp_tool:
                    logger.tool_completed(
                        func_name, duration_ms, result_type=type(result).__name__
                    )
                else:
                    logger.performance_metric(
                        "function_duration", duration_ms, "ms", function=func_name
                    )

                return result

            except Exception as e:
                duration_ms = round((time.time() - start_time) * 1000, 2)

                if is_mcp_tool:
                    logger.tool_failed(
                        func_name, str(e), duration_ms, error_type=type(e).__name__
                    )
                else:
                    logger.performance_metric(
                        "function_duration",
                        duration_ms,
                        "ms",
                        function=func_name,
                        success=False,
                        error=str(e),
                    )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                duration_ms = round((time.time() - start_time) * 1000, 2)
                logger.performance_metric(
                    "function_duration", duration_ms, "ms", function=func_name
                )
                return result

            except Exception as e:
                duration_ms = round((time.time() - start_time) * 1000, 2)
                logger.performance_metric(
                    "function_duration",
                    duration_ms,
                    "ms",
                    function=func_name,
                    success=False,
                    error=str(e),
                )
                raise

        # Return appropriate wrapper based on function type
        import asyncio

        if asyncio.iscoroutinefunction(func):
            wrapper = async_wrapper
        else:
            wrapper = sync_wrapper

        # Copy _mcp_tool attribute if it exists
        if hasattr(func, "_mcp_tool"):
            wrapper._mcp_tool = func._mcp_tool

        return wrapper

    return decorator


@contextmanager
def log_context(**context_vars):
    """
    Context manager for adding structured context to logs.

    Args:
        **context_vars: Context variables to add to all logs in this context
    """
    if STRUCTLOG_AVAILABLE:
        with structlog.contextvars.bound_contextvars(**context_vars):
            yield
    else:
        # For standard logging, we can't easily add context, so just yield
        yield


def get_mcp_logger(
    service_name: str = "mcp-server",
    level: str = "INFO",
    version: str = "1.0.0",
    context: Optional[LogContext] = None,
) -> MCPLogger:
    """
    Get a configured MCP logger instance.

    Args:
        service_name: Name of the MCP server
        level: Log level
        version: Server version
        context: Default context for this logger

    Returns:
        Configured MCPLogger instance
    """
    base_logger = setup_logging(level=level, service_name=service_name, version=version)
    return MCPLogger(base_logger, context)


# Convenience function for quick setup
def setup_mcp_logging(config) -> MCPLogger:
    """
    Setup MCP logging from configuration object.

    Args:
        config: Configuration object with log_level, server_name, and version

    Returns:
        Configured MCPLogger instance
    """
    return get_mcp_logger(
        service_name=config.server_name,
        level=config.log_level,
        version=getattr(config, "version", "1.0.0"),
    )
