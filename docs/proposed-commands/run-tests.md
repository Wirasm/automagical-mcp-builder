# Run MCP Tests

Run tests for MCP components with proper UV commands: $ARGUMENTS

## Process

1. **Parse Test Scope**
   - No arguments: Run all tests
   - Feature name: Run feature tests
   - Component type: Run specific component tests
   - File path: Run specific test file

2. **Execute Tests with UV**
   ```bash
   # All tests
   uv run pytest
   
   # Feature tests
   uv run pytest src/features/{feature_name}/
   
   # Component type tests
   uv run pytest src/features/*/tools/tests/
   uv run pytest src/features/*/resources/tests/
   uv run pytest src/features/*/prompts/tests/
   
   # Specific file
   uv run pytest {file_path}
   ```

3. **Add Appropriate Flags**
   - `-v` for verbose output
   - `-s` to show print statements
   - `--tb=short` for shorter tracebacks
   - `-k` for keyword filtering

4. **Check Coverage** (if coverage installed)
   ```bash
   uv run pytest --cov=src/features/{feature_name} --cov-report=term-missing
   ```

## Example Usage

```bash
# Run all tests
/command run-tests

# Run feature tests
/command run-tests weather_api

# Run all tool tests
/command run-tests tools

# Run specific test file
/command run-tests src/features/weather_api/tools/tests/test_get_forecast.py

# Run with verbose output
/command run-tests weather_api -v

# Run tests matching keyword
/command run-tests -k "validation"
```

## Test Patterns

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **Response Tests**: Validate standard response formats
- **Error Tests**: Ensure proper error handling

## Common Test Issues

1. **Import Errors**
   - Run `uv sync` first
   - Check absolute imports from `src/`

2. **Async Test Failures**
   - Ensure `pytest-asyncio` is installed
   - Use `@pytest.mark.asyncio` decorator

3. **Mock Issues**
   - Mock at the correct level
   - Use `patch` with full import path

## Notes

- Always run tests before committing
- Tests should be fast and isolated
- Mock external dependencies
- Follow AAA pattern: Arrange, Act, Assert