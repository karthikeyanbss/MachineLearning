#!/usr/bin/env python3
"""
MCP Server for Machine Learning Operations
This server provides tools for ML model operations via the Model Context Protocol.
"""

import asyncio
import json
from typing import Any, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Create an MCP server instance
app = Server("ml-operations")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available ML operation tools."""
    return [
        Tool(
            name="get_ml_info",
            description="Get information about the Machine Learning project",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="check_dependencies",
            description="Check if required ML dependencies are installed",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool execution requests."""
    
    if name == "get_ml_info":
        info = {
            "project": "Machine Learning - Named Entity Recognition (NER)",
            "description": "Complete, enterprise-style Named Entity Recognition project using Python and NLP techniques",
            "status": "MCP Agent installed and ready"
        }
        return [TextContent(
            type="text",
            text=json.dumps(info, indent=2)
        )]
    
    elif name == "check_dependencies":
        try:
            import numpy
            import pandas
            import sklearn
            
            deps = {
                "numpy": numpy.__version__,
                "pandas": pandas.__version__,
                "scikit-learn": sklearn.__version__,
                "status": "All core dependencies installed"
            }
            return [TextContent(
                type="text",
                text=json.dumps(deps, indent=2)
            )]
        except ImportError as e:
            return [TextContent(
                type="text",
                text=f"Missing dependency: {str(e)}\nPlease run: pip install -r requirements.txt"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
