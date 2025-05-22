# Add MCP Resource to Feature

Add a new MCP resource to an existing feature: $ARGUMENTS

## Process

1. **Parse Arguments**
   - Extract feature name and resource name
   - Format: `{feature_name}/{resource_name}`
   - Example: `weather_api/current_conditions`

2. **Validate Feature Exists**
   - Check that `src/features/{feature_name}` exists
   - Ensure the feature has a resources directory

3. **Create Resource Implementation**
   - Create `src/features/{feature_name}/resources/{resource_name}.py`
   - Include standard imports:
     ```python
     from src.data_types import MCPResourceData
     from typing import Optional
     import json
     ```
   - Define resource data model extending MCPResourceData
   - Implement resource function

4. **Create Resource Test**
   - Create `src/features/{feature_name}/resources/tests/test_{resource_name}.py`
   - Include tests for:
     - URI template parsing
     - Data format validation
     - Cache TTL settings
     - Error scenarios

5. **Register Resource in Server**
   - Update `{feature_name}_server.py` to register the resource
   - Define proper URI scheme (e.g., `weather://current/{location}`)

## Example Usage

```bash
/command add-resource weather_api/current_conditions
/command add-resource github_integration/repository_info
/command add-resource database_connector/table_schema
```

## Resource Template

```python
"""
{Resource description}
"""
from src.data_types import MCPResourceData
from typing import Optional
from datetime import datetime
import json

class {ResourceName}Data(MCPResourceData):
    """Data model for {resource_name} resource."""
    # Add resource-specific fields
    data_field: str
    timestamp: datetime
    
async def get_{resource_name}(param: str) -> str:
    """
    Get {resource description}.
    
    Args:
        param: URI parameter from template
        
    Returns:
        JSON-formatted resource data
    """
    # Fetch or generate resource data
    data = fetch_data(param)
    
    # Create resource data model
    resource_data = {ResourceName}Data(
        data_field=data['field'],
        timestamp=datetime.now(),
        cache_ttl=300,  # 5 minutes
        metadata={"source": "api"}
    )
    
    return resource_data.model_dump_json(indent=2)
```

## Resource URI Patterns

- Use descriptive schemes: `{feature}://{resource}/{params}`
- Examples:
  - `weather://current/{location}`
  - `github://repo/{owner}/{repo}`
  - `database://schema/{table}`
- Keep URIs RESTful and intuitive

## Notes

- Resources are read-only data sources
- All resources must extend MCPResourceData
- Consider caching strategies for expensive operations
- URI schemes should be intuitive and consistent