#!/usr/bin/env python3
"""
Weather MCP Server

A Model Context Protocol server that provides weather information
using the OpenWeatherMap API.
"""

import asyncio
import logging
import sys
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from tools import TOOLS, get_current_weather, get_forecast

# Configure logging to stderr (not stdout for STDIO transport)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("weather-mcp-server")

@server.list_tools()
async def list_tools() -> List[Any]:
    """List available tools"""
    logger.info("Listing available tools")
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    
    try:
        if name == "get_current_weather":
            location = arguments.get("location")
            if not location:
                return [TextContent(type="text", text="Error: location parameter is required")]
            
            result = await get_current_weather(location)
            return [TextContent(type="text", text=result)]
            
        elif name == "get_forecast":
            location = arguments.get("location")
            if not location:
                return [TextContent(type="text", text="Error: location parameter is required")]
            
            days = arguments.get("days", 5)
            result = await get_forecast(location, days)
            return [TextContent(type="text", text=result)]
            
        else:
            return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]
            
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Main entry point"""
    logger.info("Starting Weather MCP Server")
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())