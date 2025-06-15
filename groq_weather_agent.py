#!/usr/bin/env python3
"""
Groq-powered Weather AI Agent

A real AI agent using Groq's LLM that can:
1. Chat naturally with users
2. Automatically detect weather queries  
3. Call your MCP weather server to get real data
4. Provide intelligent, conversational responses
"""

import asyncio
import json
import sys
import re
import os
from typing import Dict, List, Optional, Tuple
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


class GroqWeatherAgent:
    """Real AI agent powered by Groq LLM with MCP weather integration."""
    
    def __init__(self, api_key: str):
        """Initialize the Groq AI agent."""
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"  # Fast Llama3 model
        self.conversation_history = []
        
        # US city coordinates database
        self.city_coords = {
            "new york": (40.7128, -74.0060),
            "nyc": (40.7128, -74.0060),
            "los angeles": (34.0522, -118.2437),
            "la": (34.0522, -118.2437),
            "chicago": (41.8781, -87.6298),
            "houston": (29.7604, -95.3698),
            "philadelphia": (39.9526, -75.1652),
            "phoenix": (33.4484, -112.0740),
            "san antonio": (29.4241, -98.4936),
            "san diego": (32.7157, -117.1611),
            "dallas": (32.7767, -96.7970),
            "austin": (30.2672, -97.7431),
            "san jose": (37.3382, -121.8863),
            "fort worth": (32.7555, -97.3308),
            "columbus": (39.9612, -82.9988),
            "charlotte": (35.2271, -80.8431),
            "indianapolis": (39.7684, -86.1581),
            "san francisco": (37.7749, -122.4194),
            "seattle": (47.6062, -122.3321),
            "denver": (39.7392, -104.9903),
            "washington": (38.9072, -77.0369),
            "washington dc": (38.9072, -77.0369),
            "dc": (38.9072, -77.0369),
            "boston": (42.3601, -71.0589),
            "nashville": (36.1627, -86.7816),
            "baltimore": (39.2904, -76.6122),
            "oklahoma city": (35.4676, -97.5164),
            "portland": (45.5152, -122.6784),
            "las vegas": (36.1699, -115.1398),
            "milwaukee": (43.0389, -87.9065),
            "albuquerque": (35.0844, -106.6504),
            "tucson": (32.2226, -110.9747),
            "fresno": (36.7378, -119.7871),
            "sacramento": (38.5816, -121.4944),
            "mesa": (33.4152, -111.8315),
            "kansas city": (39.0997, -94.5786),
            "atlanta": (33.7490, -84.3880),
            "omaha": (41.2565, -95.9345),
            "colorado springs": (38.8339, -104.8214),
            "raleigh": (35.7796, -78.6382),
            "miami": (25.7617, -80.1918),
            "cleveland": (41.4993, -81.6944),
            "tulsa": (36.1540, -95.9928),
            "minneapolis": (44.9778, -93.2650),
            "wichita": (37.6872, -97.3301),
            "arlington": (32.7357, -97.1081),
            "new orleans": (29.9511, -90.0715),
            "bakersfield": (35.3733, -119.0187),
            "tampa": (27.9506, -82.4572),
            "honolulu": (21.3099, -157.8581),
            "anaheim": (33.8366, -117.9143),
            "santa ana": (33.7455, -117.8677),
            "corpus christi": (27.8006, -97.3964),
            "riverside": (33.9533, -117.3961),
            "lexington": (38.0406, -84.5037),
            "pittsburgh": (40.4406, -79.9959),
            "st. louis": (38.6270, -90.1994),
            "saint louis": (38.6270, -90.1994),
            "cincinnati": (39.1031, -84.5120),
            "anchorage": (61.2181, -149.9003),
            "stockton": (37.9577, -121.2908),
            "toledo": (41.6528, -83.5379),
            "st. paul": (44.9537, -93.0900),
            "saint paul": (44.9537, -93.0900),
            "newark": (40.7357, -74.1724),
            "greensboro": (36.0726, -79.7920),
            "plano": (33.0198, -96.6989),
            "henderson": (36.0395, -114.9817),
            "lincoln": (40.8136, -96.7026),
            "buffalo": (42.8864, -78.8784),
            "jersey city": (40.7178, -74.0431),
            "chula vista": (32.6401, -117.0842),
            "fort wayne": (41.0793, -85.1394),
            "orlando": (28.5383, -81.3792),
            "st. petersburg": (27.7676, -82.6403),
            "saint petersburg": (27.7676, -82.6403),
            "chandler": (33.3062, -111.8413),
            "laredo": (27.5806, -99.4803),
            "norfolk": (36.9068, -76.2859),
            "durham": (35.9940, -78.8986),
            "madison": (43.0731, -89.4012),
            "lubbock": (33.5779, -101.8552),
            "irvine": (33.6846, -117.8265),
            "winston-salem": (36.0999, -80.2442),
            "glendale": (33.5387, -112.1860),
            "garland": (32.9126, -96.6389),
            "hialeah": (25.8576, -80.2781),
            "reno": (39.5296, -119.8138),
            "chesapeake": (36.7682, -76.2875),
            "gilbert": (33.3528, -111.7890),
            "baton rouge": (30.4515, -91.1871),
            "irving": (32.8140, -96.9489),
            "scottsdale": (33.4942, -111.9261),
            "north las vegas": (36.1989, -115.1175),
            "fremont": (37.5485, -121.9886),
            "boise": (43.6150, -116.2023),
            "richmond": (37.5407, -77.4360),
            "san bernardino": (34.1083, -117.2898),
            "birmingham": (33.5186, -86.8104),
            "spokane": (47.6587, -117.4260),
            "rochester": (43.1566, -77.6088),
            "des moines": (41.5868, -93.6250),
            "modesto": (37.6391, -120.9969),
            "fayetteville": (35.0527, -78.8784),
            "tacoma": (47.2529, -122.4443),
            "oxnard": (34.1975, -119.1771),
            "fontana": (34.0922, -117.4350),
            "columbus": (32.4609, -84.9877),
            "montgomery": (32.3668, -86.3000),
            "moreno valley": (33.9425, -117.2297),
            "shreveport": (32.5252, -93.7502),
            "aurora": (39.7294, -104.8319),
            "yonkers": (40.9312, -73.8988),
            "akron": (41.0814, -81.5190),
            "huntington beach": (33.7091, -118.0067),
            "little rock": (34.7465, -92.2896),
            "augusta": (33.4735, -82.0105),
            "amarillo": (35.2220, -101.8313),
            "glendale": (34.1425, -118.2551),
            "mobile": (30.6954, -88.0399),
            "grand rapids": (42.9634, -85.6681),
            "salt lake city": (40.7608, -111.8910),
            "tallahassee": (30.4518, -84.2807),
            "huntsville": (34.7304, -86.5861),
            "grand prairie": (32.7460, -96.9978),
            "knoxville": (35.9606, -83.9207),
            "worcester": (42.2626, -71.8023),
            "newport news": (37.0871, -76.4730),
            "brownsville": (25.9018, -97.4975),
            "overland park": (38.9822, -94.6708),
            "santa clarita": (34.3917, -118.5426),
            "providence": (41.8240, -71.4128),
            "garden grove": (33.7739, -117.9414),
            "chattanooga": (35.0456, -85.3097),
            "oceanside": (33.1959, -117.3795),
            "jackson": (32.2988, -90.1848),
            "fort lauderdale": (26.1224, -80.1373),
            "santa rosa": (38.4404, -122.7144),
            "rancho cucamonga": (34.1064, -117.5931),
            "port st. lucie": (27.2730, -80.3582),
            "tempe": (33.4255, -111.9400),
            "ontario": (34.0633, -117.6509),
            "vancouver": (45.6387, -122.6615),
            "cape coral": (26.5629, -81.9495),
            "sioux falls": (43.5446, -96.7311),
            "springfield": (37.2153, -93.2982),
            "peoria": (40.6936, -89.5890),
            "pembroke pines": (26.0070, -80.2962),
            "elk grove": (38.4088, -121.3716),
            "salem": (44.9429, -123.0351),
            "lancaster": (34.6868, -118.1542),
            "corona": (33.8753, -117.5664),
            "eugene": (44.0521, -123.0868),
            "palmdale": (34.5794, -118.1165),
            "salinas": (36.6777, -121.6555),
            "springfield": (39.7817, -89.6501),
            "pasadena": (34.1478, -118.1445),
            "fort collins": (40.5853, -105.0844),
            "hayward": (37.6688, -122.0808),
            "pomona": (34.0552, -117.7500),
            "cary": (35.7915, -78.7811),
            "rockford": (42.2711, -89.0940),
            "alexandria": (38.8048, -77.0469),
            "escondido": (33.1192, -117.0864),
            "mckinney": (33.1973, -96.6397),
            "kansas city": (39.1142, -94.6275),
            "joliet": (41.5250, -88.0817),
            "sunnyvale": (37.3688, -122.0363)
        }
        
        # State code mappings
        self.state_codes = {
            "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", 
            "california": "CA", "ca": "CA",
            "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
            "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
            "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
            "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO",
            "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
            "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH",
            "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
            "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT",
            "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY"
        }
    
    def extract_location_from_text(self, text: str) -> Optional[Tuple[str, Tuple[float, float]]]:
        """Extract location from text and return coordinates."""
        text_lower = text.lower()
        
        # Check for cities first (more specific)
        for city, coords in self.city_coords.items():
            if city in text_lower:
                return city.title(), coords
        
        return None
    
    def extract_state_from_text(self, text: str) -> Optional[str]:
        """Extract state from text and return state code."""
        text_lower = text.lower()
        
        for state_name, state_code in self.state_codes.items():
            if state_name in text_lower:
                return state_code
            # Also check for state codes directly
            if state_code.lower() in text_lower:
                return state_code
        
        return None
    
    def is_weather_query(self, text: str) -> Dict[str, any]:
        """Determine if text is a weather query and what type."""
        text_lower = text.lower()
        
        weather_keywords = ["weather", "temperature", "temp", "forecast", "rain", "snow", "sunny", "cloudy", "hot", "cold", "storm"]
        alert_keywords = ["alert", "warning", "watch", "advisory", "severe", "emergency", "danger"]
        
        has_weather = any(keyword in text_lower for keyword in weather_keywords)
        has_alert = any(keyword in text_lower for keyword in alert_keywords)
        
        if has_alert or (has_weather and any(word in text_lower for word in ["alert", "warning"])):
            # This is an alert query
            state = self.extract_state_from_text(text)
            if state:
                return {"type": "alert", "state": state}
        
        if has_weather:
            # This is a forecast query
            location = self.extract_location_from_text(text)
            if location:
                city_name, coords = location
                return {"type": "forecast", "city": city_name, "coords": coords}
        
        return {"type": None}
    
    async def get_weather_data(self, query_info: Dict[str, any]) -> str:
        """Fetch weather data using MCP server."""
        try:
            if query_info["type"] == "alert":
                state = query_info["state"]
                result = await get_alerts(state)
                return f"Weather alerts for {state}:\n{result}"
            
            elif query_info["type"] == "forecast":
                city = query_info["city"]
                lat, lng = query_info["coords"]
                result = await get_forecast(lat, lng)
                return f"Weather forecast for {city}:\n{result}"
            
        except Exception as e:
            return f"Sorry, I couldn't fetch the weather data: {e}"
        
        return "I couldn't process that weather request."
    
    async def chat_with_groq(self, user_message: str, weather_data: Optional[str] = None) -> str:
        """Chat with Groq LLM, optionally including weather data."""
        
        # Build the system message
        system_message = """You are a helpful AI assistant with access to real-time US weather data. 
        
When users ask about weather, you can provide current forecasts and alerts for US locations.
Be conversational, friendly, and helpful. If weather data is provided, incorporate it naturally into your response.
If asked about non-US locations, politely explain that you only have access to US weather data.

Keep responses concise but informative."""

        # Build messages
        messages = [{"role": "system", "content": system_message}]
        
        # Add conversation history (last 5 exchanges to keep context manageable)
        recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 10 else self.conversation_history
        messages.extend(recent_history)
        
        # Add current user message
        user_content = user_message
        if weather_data:
            user_content += f"\n\nCurrent weather data:\n{weather_data}"
        
        messages.append({"role": "user", "content": user_content})
        
        try:
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )
            
            response = completion.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            return f"Sorry, I'm having trouble connecting to my AI brain right now: {e}"
    
    async def process_message(self, user_message: str) -> str:
        """Process user message, fetch weather data if needed, and generate response."""
        
        # Check if this is a weather query
        weather_query = self.is_weather_query(user_message)
        weather_data = None
        
        if weather_query["type"]:
            print(f"🌤️  Detected weather query: {weather_query}")
            weather_data = await self.get_weather_data(weather_query)
        
        # Generate AI response
        response = await self.chat_with_groq(user_message, weather_data)
        return response
    
    async def chat_loop(self):
        """Start interactive chat loop."""
        print("🤖 Groq Weather AI Agent Ready!")
        print("Ask me anything, including weather questions for US locations.")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n🤖 Thanks for chatting! Have a great day! 👋")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 *thinking...*")
                response = await self.process_message(user_input)
                print(f"\nAI: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 Thanks for chatting! Have a great day! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


async def main():
    """Main function to run the Groq Weather AI Agent."""
    
    # Get Groq API key from environment
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        print("Please create a .env file with: GROQ_API_KEY=your_api_key_here")
        return
    
    print("🚀 Starting Groq Weather AI Agent...")
    
    try:
        # Create and start the agent
        agent = GroqWeatherAgent(api_key)
        await agent.chat_loop()
        
    except Exception as e:
        print(f"❌ Failed to start AI agent: {e}")


if __name__ == "__main__":
    print("🌟 Groq-powered Weather AI Agent")
    print("=" * 50)
    asyncio.run(main())
