<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# MCP Server Development Instructions

This is a Model Context Protocol (MCP) server project written in Python. When working on this project:

## Key Guidelines

1. **Use FastMCP**: This project uses the `mcp.server.fastmcp.FastMCP` class for easy server creation
2. **Tool Decorators**: Use `@mcp.tool()` decorator to register new tools
3. **Type Hints**: Always include proper type hints for function parameters and return types
4. **Error Handling**: Include proper error handling for API requests and data processing
5. **Documentation**: Include clear docstrings for all tools explaining their purpose and parameters

## MCP Concepts

- **Tools**: Functions that can be called by LLMs (decorated with `@mcp.tool()`)
- **Resources**: File-like data that can be read by clients
- **Prompts**: Pre-written templates for specific tasks

## References

You can find more info and examples at https://modelcontextprotocol.io/llms-full.txt

## Current Server Features

This weather server provides:
- `get_alerts`: Get weather alerts for US states
- `get_forecast`: Get weather forecast for specific coordinates

When adding new tools, follow the same pattern of async functions with proper error handling and clear documentation.
