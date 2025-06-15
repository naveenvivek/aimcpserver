#!/usr/bin/env python3
"""
Demo: Smart Weather Agent with Zero Hardcoding

Shows how LLM handles everything dynamically:
- Understands any location naturally
- Figures out coordinates on its own
- Decides when to call weather tools
- No hardcoded lists needed!
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append('/Users/naveenvivek/VSCode/MCPserver')

from smart_weather_agent import SmartGroqWeatherAgent

async def demo_smart_agent():
    """Demo the smart agent with challenging queries."""
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Please set GROQ_API_KEY in your .env file")
        return
    
    print("🧠 Smart Weather Agent Demo - No Hardcoding!")
    print("=" * 60)
    
    agent = SmartGroqWeatherAgent(api_key)
    
    # Test queries that would break hardcoded systems
    test_queries = [
        "What's the weather like in downtown Sacramento?",
        "Any severe weather warnings in the Golden State?", 
        "How's it looking in the Big Apple tomorrow?",
        "Weather forecast for the Space City",  # Houston nickname
        "Any storms coming to the Lone Star State?",  # Texas nickname
        "What's the temperature in the city by the bay?",  # San Francisco
        "Weather alerts for the Empire State?",  # New York
        "Hello! How are you doing today?",  # Non-weather query
        "Tell me about weather in London, UK",  # Non-US location
    ]
    
    print("🚀 Testing LLM's ability to understand complex queries...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"🧪 Test {i}: '{query}'")
        print("-" * 50)
        
        try:
            response = await agent.chat_with_tools(query)
            print(f"🤖 Smart Agent: {response}\n")
            
            # Wait between queries
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    print("✅ Demo completed! The LLM handled everything without hardcoding!")

if __name__ == "__main__":
    asyncio.run(demo_smart_agent())
