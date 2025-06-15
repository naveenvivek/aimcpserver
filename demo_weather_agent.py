#!/usr/bin/env python3
"""
Weather AI Agent Demo

Demonstrates the weather AI agent in action with sample queries.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append('/Users/naveenvivek/VSCode/MCPserver')

async def demo_weather_agent():
    """Demo the weather AI agent with sample queries."""
    
    print("🤖 Weather AI Agent Demo")
    print("=" * 50)
    
    try:
        # Import the simple weather agent
        from simple_weather_agent import SimpleWeatherAgent
        
        agent = SimpleWeatherAgent()
        
        # Test server connection
        if not await agent.test_weather_server():
            print("❌ Cannot connect to weather server")
            return
        
        # Demo queries
        demo_queries = [
            "alerts for California",
            "weather in Sacramento", 
            "forecast for San Francisco",
            "alerts for Texas"
        ]
        
        print("🚀 Running demo queries...\n")
        
        for i, query in enumerate(demo_queries, 1):
            print(f"Demo Query {i}: '{query}'")
            print("-" * 40)
            
            try:
                response = await agent.process_query(query)
                print(f"Agent Response:\n{response}\n")
                
                # Wait a bit between queries to be nice to the API
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Error with query '{query}': {e}\n")
        
        print("✅ Demo completed!")
        
    except ImportError as e:
        print(f"❌ Cannot import weather agent: {e}")
    except Exception as e:
        print(f"❌ Demo error: {e}")


async def interactive_mode():
    """Run the agent in interactive mode."""
    try:
        from simple_weather_agent import SimpleWeatherAgent
        
        agent = SimpleWeatherAgent()
        
        if await agent.test_weather_server():
            await agent.chat_loop()
        else:
            print("❌ Cannot start interactive mode - server test failed")
            
    except ImportError as e:
        print(f"❌ Cannot import weather agent: {e}")


async def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await interactive_mode()
    else:
        await demo_weather_agent()


if __name__ == "__main__":
    print("🌤️  Weather AI Agent System")
    print("Usage:")
    print("  python3 demo_weather_agent.py          # Run demo")
    print("  python3 demo_weather_agent.py --interactive  # Interactive mode")
    print()
    
    asyncio.run(main())
