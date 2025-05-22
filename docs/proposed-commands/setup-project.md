# Setup MCP Builder Project

Setup the MCP Builder project for proper development with editable installs and import resolution.

## Process

1. **Ensure UV is Installed**
   ```bash
   # Check if UV is installed
   which uv || curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create Virtual Environment**
   ```bash
   uv venv
   ```

3. **Install Dependencies**
   ```bash
   # Install all dependencies from pyproject.toml
   uv sync
   ```

4. **Install Project as Editable**
   ```bash
   # Install the project itself in editable mode
   uv pip install -e .
   ```

5. **Verify Installation**
   - Check that imports work correctly
   - Test running the main server
   - Ensure all features can import shared modules

6. **Setup Environment File**
   ```bash
   # Copy example environment file if it exists
   if [ -f .env.example ]; then
       cp .env.example .env
       echo "Created .env file from example"
   fi
   ```

## Post-Setup Verification

Run these commands to verify setup:

```bash
# Test imports
uv run python -c "from src.logging_config import setup_mcp_logging; print('✓ Logging imports work')"
uv run python -c "from src.data_types import success_response; print('✓ Data types import work')"

# Test server startup
uv run python src/main_server.py --help

# Run tests
uv run pytest src/features/hello_world/
```

## Common Setup Issues

1. **Import Errors After Setup**
   - Ensure `uv pip install -e .` was run
   - Check that pyproject.toml has correct package configuration
   - Verify virtual environment is activated

2. **UV Not Found**
   - Install UV using the curl command
   - Add UV to PATH if needed

3. **Permission Errors**
   - Use appropriate permissions for install directories
   - Consider using `--user` flag if needed

## Notes

- This setup enables absolute imports from `src/`
- Editable install means code changes take effect immediately
- Virtual environment isolation prevents conflicts
- Always run commands with `uv run` prefix