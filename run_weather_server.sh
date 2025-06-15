#!/bin/bash
# Weather MCP Server Launcher
# This script ensures the correct environment is set up

cd "/Users/naveenvivek/VSCode/MCPserver"
export PATH="/Users/naveenvivek/.local/bin:$PATH"
exec uv run weather_server.py
