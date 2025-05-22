# Validate MCP Feature

Validate that an MCP feature follows all project standards and conventions: $ARGUMENTS

## Process

1. **Check Directory Structure**
   - Verify all required directories exist:
     - `api/`, `tools/`, `resources/`, `prompts/`
     - Each with corresponding `tests/` subdirectory
   - Ensure all `__init__.py` files are present

2. **Validate Naming Conventions**
   - Feature directory: snake_case
   - Server file: `{feature_name}_server.py`
   - Config file: `config.py`
   - Test files: `test_{component_name}.py`

3. **Check Import Patterns**
   - No manual sys.path manipulation
   - Absolute imports from `src/` for shared modules
   - Proper import ordering in all files

4. **Validate Components**
   - **Tools**:
     - Return standardized responses
     - Have proper type hints
     - Include docstrings
     - Have corresponding tests
   
   - **Resources**:
     - Extend MCPResourceData
     - Follow URI template patterns
     - Include cache TTL settings
     - Have corresponding tests
   
   - **Prompts**:
     - Use MCPPromptTemplate structure
     - Include parameter validation
     - Have corresponding tests

5. **Check Configuration**
   - Config class extends BaseSettings
   - Environment variable prefix matches feature
   - All required settings defined

6. **Validate Tests**
   - All components have tests
   - Tests are co-located correctly
   - Test both success and error cases
   - Mock external dependencies

7. **Check Server Implementation**
   - Uses FastMCP framework
   - Implements standardized logging
   - Proper error handling
   - All components registered

## Example Usage

```bash
/command validate-feature weather_api
/command validate-feature github_integration
```

## Validation Checklist

```
✓ Directory structure complete
✓ All __init__.py files present
✓ Naming conventions followed
✓ No sys.path manipulation
✓ Proper import patterns
✓ Tools return standard responses
✓ Resources extend MCPResourceData
✓ All components have tests
✓ Tests co-located correctly
✓ Configuration properly structured
✓ Server uses FastMCP
✓ Logging implemented correctly
✓ Error handling standardized
```

## Notes

- This validation ensures consistency across all features
- Run before committing new features
- Fix any issues before proceeding with implementation
- Use alongside pytest for complete validation