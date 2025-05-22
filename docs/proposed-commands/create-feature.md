# Create New MCP Feature

Create a complete MCP feature structure with all required directories and files: $ARGUMENTS

## Process

1. **Parse Feature Name**
   - Extract feature name from arguments
   - Ensure it follows snake_case convention
   - Validate it doesn't already exist

2. **Create Directory Structure**
   ```
   src/features/{feature_name}/
   ├── __init__.py
   ├── config.py                    # Feature configuration
   ├── {feature_name}_server.py     # Main server implementation
   ├── api/
   │   ├── __init__.py
   │   └── tests/
   │       └── __init__.py
   ├── tools/
   │   ├── __init__.py
   │   └── tests/
   │       └── __init__.py
   ├── resources/
   │   ├── __init__.py
   │   └── tests/
   │       └── __init__.py
   └── prompts/
       ├── __init__.py
       └── tests/
           └── __init__.py
   ```

3. **Create Base Configuration File**
   - Generate `config.py` with standard configuration class
   - Include transport settings and feature toggles
   - Follow the hello_world pattern

4. **Create Server Entry Point**
   - Generate `{feature_name}_server.py` with FastMCP setup
   - Include proper imports (using absolute imports)
   - Add basic server initialization

5. **Create Example Components**
   - Add one example tool with test
   - Add one example resource with test
   - Add one example prompt with test

6. **Update Project Files**
   - Add feature to pyproject.toml packages list
   - Create entry point script if needed

## Example Usage

```bash
/command create-feature weather_api
/command create-feature github_integration
/command create-feature database_connector
```

## Notes

- Feature names should be descriptive and follow snake_case
- All created files will follow project conventions from CLAUDE.md
- Tests will be co-located with their components
- The feature will be ready for implementation after creation