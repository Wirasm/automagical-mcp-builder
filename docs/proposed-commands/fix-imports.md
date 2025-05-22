# Fix Python Import Issues

Fix Python import management issues in the MCP Builder project for file: $ARGUMENTS

## Process

1. **Analyze Current Import Structure**
   - Check if the file has path manipulation code
   - Identify all imports from project modules
   - Detect any circular import risks

2. **Fix Import Patterns**
   - Remove manual sys.path manipulation
   - Convert to absolute imports from `src/`
   - Ensure proper import ordering:
     - Standard library imports
     - Third-party imports (mcp, pydantic, etc.)
     - Local project imports

3. **Update Import Statements**
   ```python
   # Remove this pattern:
   import sys
   from pathlib import Path
   src_path = Path(__file__).parent.parent.parent
   if str(src_path) not in sys.path:
       sys.path.insert(0, str(src_path))
   
   # Replace with:
   from src.logging_config import setup_mcp_logging, MCPLogger
   from src.data_types import success_response, error_response
   ```

4. **Fix Relative Imports Within Features**
   - Keep relative imports for intra-feature modules
   - Use absolute imports for cross-feature or shared modules

5. **Validate Changes**
   - Ensure all imports resolve correctly
   - Check for unused imports
   - Verify no circular dependencies

## Example Usage

```bash
/command fix-imports src/features/hello_world/hello_world_server.py
/command fix-imports src/features/weather_api/tools/get_forecast.py
```

## Notes

- This command assumes the project is properly installed with `uv pip install -e .`
- All feature modules should use absolute imports from `src/`
- Shared modules (logging_config, data_types) must always be imported absolutely