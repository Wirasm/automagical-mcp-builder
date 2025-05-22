#!/usr/bin/env python3
"""
Main MCP Builder server entry point.
Routes to the hello_world feature server for this basic template.
"""

import sys
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import the FastMCP server object and main function
from features.hello_world.server import main, mcp as hello_world_mcp  # noqa: E402

# Expose FastMCP server globally for mcp install command
mcp = hello_world_mcp

if __name__ == "__main__":
    main()
