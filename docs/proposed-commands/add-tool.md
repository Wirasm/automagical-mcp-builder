# Add MCP Tool to Feature

Add a new MCP tool to an existing feature: $ARGUMENTS

## Process

1. **Parse Arguments**
   - Extract feature name and tool name
   - Format: `{feature_name}/{tool_name}`
   - Example: `weather_api/get_forecast`

2. **Validate Feature Exists**
   - Check that `src/features/{feature_name}` exists
   - Ensure the feature has a tools directory

3. **Create Tool Implementation**
   - Create `src/features/{feature_name}/tools/{tool_name}.py`
   - Include standard imports:
     ```python
     from src.logging_config import log_performance, MCPLogger
     from src.data_types import success_response, error_response, ErrorCode
     ```
   - Implement tool function with proper type hints and docstring

4. **Create Tool Test**
   - Create `src/features/{feature_name}/tools/tests/test_{tool_name}.py`
   - Include basic test structure:
     - Test successful execution
     - Test input validation
     - Test error handling
     - Test response format

5. **Register Tool in Server**
   - Update `{feature_name}_server.py` to import and register the tool
   - Ensure proper logging and error handling

## Example Usage

```bash
/command add-tool weather_api/get_forecast
/command add-tool github_integration/create_issue
/command add-tool database_connector/execute_query
```

## Tool Template

```python
"""
{Tool description}
"""
from typing import Optional
from src.logging_config import log_performance
from src.data_types import success_response, error_response, ErrorCode

async def {tool_name}(param1: str, param2: Optional[str] = None) -> dict:
    """
    {Tool description for LLM}
    
    Args:
        param1: Description
        param2: Optional description
        
    Returns:
        Standardized response dictionary
    """
    try:
        # Input validation
        if not param1.strip():
            return error_response(
                ErrorCode.VALIDATION_ERROR,
                "param1 is required"
            ).model_dump()
        
        # Tool logic here
        result = process_something(param1, param2)
        
        return success_response(
            data=result,
            message="Operation completed successfully"
        ).model_dump()
        
    except Exception as e:
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            str(e)
        ).model_dump()
```

## Notes

- Tool names should be descriptive verbs (e.g., get_forecast, create_issue)
- All tools must return standardized responses
- Tests are mandatory for all tools
- Tools should be focused on a single operation