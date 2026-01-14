#!/usr/bin/env python3
"""
MCP Server Startup Script
Starts the MCP server for task management tools
"""
import uvicorn
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.chatbot.mcp_server import create_mcp_server

if __name__ == "__main__":
    print("Starting MCP Server for Todo Task Management...")
    print("Available tools: add_task, list_tasks, complete_task, update_task, delete_task")

    # Create the server instance
    mcp_server = create_mcp_server()

    # Run the MCP server
    uvicorn.run(
        "src.chatbot.mcp_server:create_mcp_server",
        factory=True,
        host="0.0.0.0",
        port=3001,
        reload=True
    )