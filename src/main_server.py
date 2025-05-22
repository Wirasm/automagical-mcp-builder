#!/usr/bin/env python3
"""
Main MCP Builder server entry point.
Routes to the hello_world feature server for this basic template.
"""

import sys
from pathlib import Path

# Add the project root to Python path for src imports
# This is needed when running via Claude Desktop or other external processes
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import the FastMCP server object and main function
from src.features.hello_world.hello_world_server import main, mcp as hello_world_mcp  # noqa: E402

# Expose FastMCP server globally for mcp install command
mcp = hello_world_mcp

if __name__ == "__main__":
    main()
