#!/usr/bin/env python3
"""
Smart Groq Weather AI Agent - No Hardcoding!

Uses LLM's intelligence to:
- Understand any location query naturally
- Decide when to call weather tools
- Handle edge cases and errors gracefully
- No hardcoded city lists or state mappings needed!
"""

import asyncio
import json
import os
import sys
from typing import Dict, List, Optional
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path for weather server imports
sys.path.append('/Users/naveenvivek/VSCode/MCPserver')

try:
    from weather_server import get_alerts, get_forecast
except ImportError:
    print("❌ Could not import weather server functions. Make sure weather_server.py exists.")
    sys.exit(1)


class SmartGroqWeatherAgent:
    """LLM-powered weather agent with zero hardcoding."""
    
    def __init__(self, api_key: str):
        """Initialize the smart agent."""
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"
        self.conversation_history = []
        
        # Tool definitions for the LLM
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather_forecast",
                    "description": "Get weather forecast for any US location using latitude and longitude coordinates",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "type": "number",
                                "description": "Latitude coordinate of the location"
                            },
                            "longitude": {
                                "type": "number", 
                                "description": "Longitude coordinate of the location"
                            },
                            "location_name": {
                                "type": "string",
                                "description": "Human-readable name of the location"
                            }
                        },
                        "required": ["latitude", "longitude", "location_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather_alerts",
                    "description": "Get weather alerts and warnings for a US state",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "state_code": {
                                "type": "string",
                                "description": "Two-letter US state code (e.g., CA, TX, NY)"
                            },
                            "state_name": {
                                "type": "string",
                                "description": "Full name of the state"
                            }
                        },
                        "required": ["state_code", "state_name"]
                    }
                }
            }
        ]
    
    async def call_weather_function(self, function_name: str, arguments: Dict) -> str:
        """Execute weather tool functions."""
        try:
            if function_name == "get_weather_forecast":
                lat = arguments["latitude"]
                lng = arguments["longitude"]
                location = arguments["location_name"]
                
                result = await get_forecast(lat, lng)
                return f"Weather forecast for {location}:\n{result}"
            
            elif function_name == "get_weather_alerts":
                state_code = arguments["state_code"]
                state_name = arguments["state_name"]
                
                result = await get_alerts(state_code)
                return f"Weather alerts for {state_name} ({state_code}):\n{result}"
            
        except Exception as e:
            return f"Error getting weather data: {e}"
        
        return "Unknown weather function requested"
    
    async def chat_with_tools(self, user_message: str) -> str:
        """Chat with LLM using function calling for weather tools."""
        
        # System message that teaches the LLM how to use tools
        system_message = """You are a helpful weather assistant with access to real-time US weather data.

You have two tools available:
1. get_weather_forecast: Get detailed weather forecasts using coordinates
2. get_weather_alerts: Get weather alerts using state codes

When users ask about weather:
- For forecasts: You need latitude/longitude coordinates. Use your knowledge to determine coordinates for US cities.
- For alerts: You need the 2-letter state code (CA, TX, NY, etc.)

Important guidelines:
- Only use tools for US locations (the weather API only covers the US)
- Be conversational and helpful
- If you don't know coordinates, make your best estimate or ask the user
- For non-US locations, politely explain the limitation
- Always provide the location name when calling forecast tools

Examples:
- "Weather in Sacramento" → Use coordinates ~38.58, -121.49
- "Alerts for California" → Use state code "CA"
- "Weather in London" → Explain US-only limitation"""

        # Build messages with conversation history
        messages = [{"role": "system", "content": system_message}]
        
        # Add recent conversation history
        if self.conversation_history:
            messages.extend(self.conversation_history[-10:])  # Last 10 messages
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # First LLM call - let it decide if tools are needed
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",  # Let LLM decide when to use tools
                max_tokens=1000,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message
            
            # Check if LLM wants to use tools
            if assistant_message.tool_calls:
                # Execute tool calls
                tool_results = []
                
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 LLM calling: {function_name} with {arguments}")
                    
                    result = await self.call_weather_function(function_name, arguments)
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": result
                    })
                
                # Add assistant message and tool results to conversation
                messages.append({
                    "role": "assistant", 
                    "content": assistant_message.content,
                    "tool_calls": assistant_message.tool_calls
                })
                messages.extend(tool_results)
                
                # Second LLM call to synthesize final response
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                final_content = final_response.choices[0].message.content
                
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": final_content})
                
                return final_content
            
            else:
                # No tools needed, return direct response
                content = assistant_message.content
                
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": content})
                
                return content
        
        except Exception as e:
            return f"Sorry, I'm having trouble processing your request: {e}"
    
    async def chat_loop(self):
        """Interactive chat loop."""
        print("🤖 Smart Weather AI Agent Ready!")
        print("Ask me about weather anywhere in the US - I'll figure out the details!")
        print("Examples: 'Weather in downtown Seattle', 'Any storms in Florida?', 'How's the weather?'")
        print("Type 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n🤖 Thanks for chatting! Stay safe! 👋")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 *thinking...*")
                response = await self.chat_with_tools(user_input)
                print(f"\nAI: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 Thanks for chatting! Stay safe! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


async def main():
    """Run the smart weather agent."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Please set GROQ_API_KEY in your .env file")
        print("Get your free API key from: https://console.groq.com/keys")
        return
    
    print("🚀 Starting Smart Weather AI Agent...")
    
    try:
        agent = SmartGroqWeatherAgent(api_key)
        await agent.chat_loop()
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")


if __name__ == "__main__":
    print("🌟 Smart Groq Weather Agent - Zero Hardcoding!")
    print("=" * 60)
    asyncio.run(main())
