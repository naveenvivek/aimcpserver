#!/usr/bin/env python3
"""
Simple Weather AI Agent Test

A simplified version to test MCP communication with your weather server.
"""

import asyncio
import subprocess
import sys
import os

class SimpleWeatherAgent:
    """Simple AI agent that directly calls your weather MCP server."""
    
    def __init__(self):
        self.server_script = "/Users/naveenvivek/VSCode/MCPserver/run_weather_server.sh"
    
    async def test_weather_server(self):
        """Test the weather server by running it directly."""
        print("🧪 Testing weather server connection...")
        
        try:
            # Test if the server script exists and is executable
            if not os.path.exists(self.server_script):
                print(f"❌ Server script not found: {self.server_script}")
                return False
            
            if not os.access(self.server_script, os.X_OK):
                print(f"❌ Server script not executable: {self.server_script}")
                return False
            
            print("✅ Server script found and executable")
            return True
            
        except Exception as e:
            print(f"❌ Error testing server: {e}")
            return False
    
    def parse_simple_query(self, query: str):
        """Parse simple weather queries."""
        query_lower = query.lower()
        
        # Check for alerts
        if "alert" in query_lower or "warning" in query_lower:
            if "california" in query_lower or "ca" in query_lower:
                return ("alerts", "CA")
            elif "texas" in query_lower or "tx" in query_lower:
                return ("alerts", "TX")
            elif "new york" in query_lower or "ny" in query_lower:
                return ("alerts", "NY")
        
        # Check for forecasts
        if "forecast" in query_lower or "weather" in query_lower:
            if "sacramento" in query_lower:
                return ("forecast", (38.5816, -121.4944))
            elif "san francisco" in query_lower:
                return ("forecast", (37.7749, -122.4194))
            elif "new york" in query_lower:
                return ("forecast", (40.7128, -74.0060))
        
        return (None, None)
    
    async def get_weather_alerts(self, state_code: str):
        """Get weather alerts using your weather server tools."""
        # For now, we'll call the weather server functions directly
        # since MCP protocol communication is complex
        
        try:
            # Import your weather server functions
            sys.path.append('/Users/naveenvivek/VSCode/MCPserver')
            from weather_server import get_alerts
            
            result = await get_alerts(state_code)
            return result
            
        except Exception as e:
            return f"Error getting alerts: {e}"
    
    async def get_weather_forecast(self, coordinates):
        """Get weather forecast using your weather server tools."""
        try:
            # Import your weather server functions
            sys.path.append('/Users/naveenvivek/VSCode/MCPserver')
            from weather_server import get_forecast
            
            lat, lng = coordinates
            result = await get_forecast(lat, lng)
            return result
            
        except Exception as e:
            return f"Error getting forecast: {e}"
    
    async def process_query(self, query: str):
        """Process a weather query and return results."""
        print(f"🤔 Processing: '{query}'")
        
        query_type, params = self.parse_simple_query(query)
        
        if query_type == "alerts":
            print(f"📋 Getting weather alerts for {params}")
            result = await self.get_weather_alerts(params)
            return f"🚨 Weather Alerts for {params}:\n\n{result}"
        
        elif query_type == "forecast":
            lat, lng = params
            print(f"🌤️  Getting forecast for {lat}, {lng}")
            result = await self.get_weather_forecast(params)
            return f"📊 Weather Forecast:\n\n{result}"
        
        else:
            return "❓ I can help with:\n• Weather alerts (e.g., 'alerts for California')\n• Weather forecasts (e.g., 'weather in Sacramento')"
    
    async def chat_loop(self):
        """Start a simple chat loop."""
        print("🌤️  Simple Weather AI Agent Ready!")
        print("Try asking about:")
        print("• 'alerts for California' or 'alerts for Texas'")
        print("• 'weather in Sacramento' or 'forecast for San Francisco'")
        print("Type 'quit' to exit.\n")
        
        while True:
            try:
                query = input("You: ").strip()
                
                if query.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if not query:
                    continue
                
                response = await self.process_query(query)
                print(f"\nWeather Agent: {response}\n")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


async def main():
    """Run the simple weather agent."""
    agent = SimpleWeatherAgent()
    
    # Test server connection
    if await agent.test_weather_server():
        print("🚀 Starting simple weather chat...")
        await agent.chat_loop()
    else:
        print("❌ Cannot start agent - server test failed")


if __name__ == "__main__":
    asyncio.run(main())
