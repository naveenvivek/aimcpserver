# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information using the National Weather Service API.

## Features

This MCP server provides two main tools:

- **get_alerts**: Get weather alerts for US states
- **get_forecast**: Get weather forecast for specific coordinates (latitude/longitude)

## Installation

1. Make sure you have Python 3.10+ installed
2. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Install dependencies:
   ```bash
   uv add "mcp[cli]" httpx
   ```

## Usage

### Running the Server

```bash
uv run weather_server.py
```

### Testing the Server

```bash
python3 test_server.py
```

### Integrating with Claude Desktop

1. Open your Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add this server configuration:
   ```json
   {
     "mcpServers": {
       "weather": {
         "command": "uv",
         "args": [
           "--directory",
           "/ABSOLUTE/PATH/TO/YOUR/PROJECT",
           "run",
           "weather_server.py"
         ]
       }
     }
   }
   ```

3. Replace `/ABSOLUTE/PATH/TO/YOUR/PROJECT` with the actual path to this project

4. Restart Claude Desktop

## Example Queries

Once connected to Claude Desktop, you can ask:

- "What's the weather forecast for Sacramento, CA?"
- "Are there any weather alerts for Texas?"
- "What's the forecast for latitude 37.7749, longitude -122.4194?"

## API Details

This server uses the National Weather Service API:
- Base URL: `https://api.weather.gov`
- Only supports US locations
- No API key required
- Rate limits apply

## Development

This project uses:
- **Python 3.13+**
- **FastMCP**: For easy MCP server creation
- **httpx**: For async HTTP requests
- **uv**: For fast package management

### Project Structure

```
MCPserver/
├── weather_server.py           # Main MCP server
├── simple_weather_agent.py     # AI agent for natural language queries
├── demo_weather_agent.py       # Demo script for the AI agent
├── test_server.py              # Server test script
├── run_weather_server.sh       # Shell script to run the server
├── pyproject.toml              # Project configuration
├── uv.lock                     # Dependency lock file
├── .vscode/
│   ├── mcp.json                # VS Code MCP configuration
│   └── tasks.json              # VS Code tasks
└── .github/
    └── copilot-instructions.md # Copilot instructions
```

### Adding New Tools

To add new tools to this MCP server:

1. Create an async function
2. Decorate it with `@mcp.tool()`
3. Include proper type hints and docstring
4. Add error handling

Example:
```python
@mcp.tool()
async def my_new_tool(param: str) -> str:
    """Description of what this tool does.
    
    Args:
        param: Description of the parameter
    """
    # Your implementation here
    return "result"
```

## License

This project is open source and available under the MIT License.
