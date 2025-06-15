#!/usr/bin/env python3
"""
Demo script for the Groq Weather AI Agent
Shows automated conversations with the AI agent
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append('/Users/naveenvivek/VSCode/MCPserver')

from groq_weather_agent import GroqWeatherAgent

async def demo_conversation():
    """Demo conversation with the AI agent."""
    
    # Get Groq API key from environment
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        print("Please create a .env file with: GROQ_API_KEY=your_api_key_here")
        return
    
    print("🤖 Groq Weather AI Agent Demo")
    print("=" * 50)
    
    try:
        agent = GroqWeatherAgent(api_key)
        
        # Demo queries
        queries = [
            "Hello! How are you?",
            "What's the weather like in Sacramento?",
            "Are there any weather alerts for California?", 
            "Tell me about the forecast in New York",
            "Thanks, that was helpful!"
        ]
        
        print("🚀 Starting demo conversation...\n")
        
        for i, query in enumerate(queries, 1):
            print(f"Demo Query {i}: '{query}'")
            print("-" * 40)
            
            response = await agent.process_message(query)
            print(f"AI Agent: {response}\n")
            
            # Wait between queries
            await asyncio.sleep(1)
        
        print("✅ Demo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    asyncio.run(demo_conversation())
