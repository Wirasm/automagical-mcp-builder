"""
MCP Builder Data Types and Response Standards.

Provides standardized data types, response formats, and validation patterns
for all MCP servers built with this template.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, field_serializer


class ResponseStatus(str, Enum):
    """Standard response status values."""

    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    PARTIAL = "partial"


class ErrorCode(str, Enum):
    """Standard error codes for MCP operations."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    EXTERNAL_API_ERROR = "EXTERNAL_API_ERROR"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"


class MCPToolResponse(BaseModel):
    """
    Standard response format for all MCP tools.

    This ensures consistent response structure across all tools,
    making it easier for LLMs to parse and understand results.
    """

    status: ResponseStatus
    data: Optional[Any] = None
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize timestamp to ISO format."""
        return value.isoformat()

    def to_json_string(self, **kwargs) -> str:
        """Convert response to JSON string."""
        return self.model_dump_json(exclude_none=True, **kwargs)


class MCPErrorResponse(BaseModel):
    """
    Standard error response format for MCP operations.

    Provides detailed error information while maintaining
    consistency across all error scenarios.
    """

    status: ResponseStatus = ResponseStatus.ERROR
    error_code: ErrorCode
    error_message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    correlation_id: Optional[str] = None

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize timestamp to ISO format."""
        return value.isoformat()

    def to_json_string(self, **kwargs) -> str:
        """Convert error response to JSON string."""
        return self.model_dump_json(exclude_none=True, **kwargs)


class MCPResourceData(BaseModel):
    """
    Base class for standardized resource data.

    All MCP resources should extend this class to ensure
    consistent metadata and structure.
    """

    content_type: str = "application/json"
    last_updated: datetime = Field(default_factory=datetime.now)
    cache_ttl: Optional[int] = None  # TTL in seconds
    metadata: Optional[Dict[str, Any]] = None

    @field_serializer("last_updated")
    def serialize_last_updated(self, value: datetime) -> str:
        """Serialize last_updated to ISO format."""
        return value.isoformat()


class MCPPromptTemplate(BaseModel):
    """
    Standard structure for MCP prompt templates.

    Ensures prompts have consistent metadata and
    parameter validation.
    """

    template: str
    parameters: Dict[str, Any]
    description: Optional[str] = None
    category: Optional[str] = None
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.now)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        """Serialize created_at to ISO format."""
        return value.isoformat()

    def render(self, **kwargs) -> str:
        """Render the template with provided parameters."""
        return self.template.format(**kwargs)


# Input validation models for common use cases


class TextInput(BaseModel):
    """Standard input validation for text-based tools."""

    text: str = Field(..., min_length=1, max_length=10000)

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        return v.strip()


class UserIdentifier(BaseModel):
    """Standard validation for user identification."""

    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = None
    user_id: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_validation(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_validation(cls, v):
        if v and "@" not in v:
            raise ValueError("Invalid email format")
        return v


class FileInput(BaseModel):
    """Standard validation for file-related operations."""

    filename: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    content_type: Optional[str] = None
    size_bytes: Optional[int] = None

    @field_validator("filename")
    @classmethod
    def filename_validation(cls, v):
        # Basic filename validation
        invalid_chars = ["<", ">", ":", '"', "|", "?", "*"]
        if any(char in v for char in invalid_chars):
            raise ValueError("Filename contains invalid characters")
        return v.strip()


class URLInput(BaseModel):
    """Standard validation for URL inputs."""

    url: str = Field(..., min_length=1)
    validate_ssl: bool = True
    timeout_seconds: int = Field(default=30, ge=1, le=300)

    @field_validator("url")
    @classmethod
    def url_validation(cls, v):
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class PaginationInput(BaseModel):
    """Standard pagination parameters."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$")


# Response data models for common use cases


class PaginatedResponse(BaseModel):
    """Standard paginated response structure."""

    items: List[Any]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(cls, items: List[Any], total_count: int, page: int, page_size: int):
        """Helper to create paginated response."""
        total_pages = (total_count + page_size - 1) // page_size
        return cls(
            items=items,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


class FileMetadata(BaseModel):
    """Standard file metadata structure."""

    filename: str
    size_bytes: int
    content_type: str
    created_at: datetime
    modified_at: datetime
    checksum: Optional[str] = None

    @field_serializer("created_at", "modified_at")
    def serialize_datetime_fields(self, value: datetime) -> str:
        """Serialize datetime fields to ISO format."""
        return value.isoformat()


class APIHealth(BaseModel):
    """Standard API health check response."""

    status: str
    timestamp: datetime
    version: str
    uptime_seconds: int
    dependencies: Dict[str, str]  # service_name -> status

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize timestamp to ISO format."""
        return value.isoformat()


# Utility functions for response creation


def success_response(
    data: Any = None,
    message: str = "Operation completed successfully",
    metadata: Optional[Dict[str, Any]] = None,
) -> MCPToolResponse:
    """Create a standardized success response."""
    return MCPToolResponse(
        status=ResponseStatus.SUCCESS, data=data, message=message, metadata=metadata
    )


def error_response(
    error_code: ErrorCode,
    error_message: str,
    details: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None,
) -> MCPErrorResponse:
    """Create a standardized error response."""
    return MCPErrorResponse(
        error_code=error_code,
        error_message=error_message,
        details=details,
        correlation_id=correlation_id,
    )


def warning_response(
    data: Any = None,
    message: str = "Operation completed with warnings",
    metadata: Optional[Dict[str, Any]] = None,
) -> MCPToolResponse:
    """Create a standardized warning response."""
    return MCPToolResponse(
        status=ResponseStatus.WARNING, data=data, message=message, metadata=metadata
    )


def partial_response(
    data: Any = None,
    message: str = "Operation partially completed",
    metadata: Optional[Dict[str, Any]] = None,
) -> MCPToolResponse:
    """Create a standardized partial success response."""
    return MCPToolResponse(
        status=ResponseStatus.PARTIAL, data=data, message=message, metadata=metadata
    )


# Type conversion utilities


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely parse JSON string with fallback."""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def serialize_for_llm(data: Any) -> str:
    """
    Serialize data for LLM consumption.

    Converts complex data structures to JSON strings that are
    easy for LLMs to parse and understand.
    """
    if isinstance(data, BaseModel):
        return data.model_dump_json(exclude_none=True, indent=2)
    elif isinstance(data, (dict, list)):
        return json.dumps(data, indent=2, default=str)
    else:
        return str(data)


# Validation utilities


def validate_tool_input(input_model: BaseModel, raw_data: Dict[str, Any]) -> BaseModel:
    """
    Validate and parse tool input using Pydantic model.

    Args:
        input_model: Pydantic model class for validation
        raw_data: Raw input data dictionary

    Returns:
        Validated model instance

    Raises:
        ValueError: If validation fails
    """
    try:
        return input_model(**raw_data)
    except Exception as e:
        raise ValueError(f"Input validation failed: {str(e)}")


def create_schema_documentation(model: BaseModel) -> Dict[str, Any]:
    """
    Generate schema documentation for a Pydantic model.

    Useful for creating API documentation and help text.
    """
    schema = model.model_json_schema()
    return {
        "title": schema.get("title", "Unknown"),
        "description": schema.get("description", "No description available"),
        "properties": schema.get("properties", {}),
        "required": schema.get("required", []),
        "example": model.model_dump() if hasattr(model, "model_dump") else {},
    }
