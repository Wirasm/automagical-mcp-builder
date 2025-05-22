# Fix MCP Logging Issues

Fix logging configuration to ensure MCP servers work correctly with Claude Desktop and other MCP clients.

## The Problem

MCP servers communicate using JSON-RPC 2.0 protocol over stdout. When logging messages are sent to stdout, they interfere with the protocol and cause parsing errors like:
- "Invalid literal value, expected \"2.0\""
- "Unrecognized key(s) in object: 'timestamp', 'level', 'service', 'message'"

## Process

1. **Identify Logging Output Issues**
   - Check all logging configurations
   - Find any print() statements
   - Locate any stdout usage

2. **Fix Logging Configuration**
   ```python
   # BAD - Logs to stdout
   handler = logging.StreamHandler(sys.stdout)
   
   # GOOD - Logs to stderr
   handler = logging.StreamHandler(sys.stderr)
   ```

3. **Fix Print Statements**
   ```python
   # BAD - Prints to stdout
   print("Debug message")
   
   # GOOD - Prints to stderr
   print("Debug message", file=sys.stderr)
   
   # BETTER - Use logging
   logger.debug("Debug message")
   ```

4. **Fix Structlog Configuration**
   ```python
   # Ensure structlog uses stderr
   logger_factory=structlog.PrintLoggerFactory(file=sys.stderr)
   ```

5. **Verify FastMCP Server Output**
   - Ensure server only outputs JSON-RPC messages to stdout
   - All logging, debugging, and info messages go to stderr

## Common Fixes Applied

### 1. Update logging_config.py
- Change `StreamHandler(sys.stdout)` to `StreamHandler(sys.stderr)`
- Update structlog factory to use stderr

### 2. Update config.py
- Change all print() calls to use `file=sys.stderr`
- Or replace with proper logging calls

### 3. Check Feature Servers
- Ensure no print() statements in server code
- Verify all logging uses the centralized logging config

## Testing the Fix

After applying fixes:

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector python src/main_server.py

# Test with Claude Desktop
# The server should now work without JSON-RPC parsing errors
```

## Prevention

1. **Always use logging module** instead of print()
2. **Configure logging to stderr** for all MCP servers
3. **Test with MCP Inspector** before deploying
4. **Never output non-JSON-RPC to stdout** in MCP servers

## Example Usage

```bash
# Fix logging issues in a specific file
/command fix-mcp-logging src/features/weather_api/weather_api_server.py

# Fix all logging issues in project
/command fix-mcp-logging
```

## Notes

- This is a critical fix for MCP server compatibility
- The issue often appears as Zod validation errors in Claude Desktop
- Proper logging separation is required by the MCP protocol specification