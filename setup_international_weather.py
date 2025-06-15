#!/usr/bin/env python3
"""
Setup script for International Weather MCP Server
"""

import os
import asyncio
import sys

def setup_api_key():
    """Guide user through API key setup."""
    print("🌍 International Weather MCP Server Setup")
    print("=" * 50)
    
    # Check if API key already exists
    existing_key = os.getenv("OPENWEATHER_API_KEY")
    if existing_key:
        print(f"✅ API key already set: {existing_key[:8]}...")
        return existing_key
    
    print("\n📋 To use this weather server, you need a free OpenWeatherMap API key:")
    print("1. Go to: https://openweathermap.org/api")
    print("2. Click 'Sign Up' and create a free account")
    print("3. After login, go to 'API keys' section")
    print("4. Copy your API key")
    print("5. Come back here and enter it")
    
    print("\n💡 The free tier includes:")
    print("   • 1,000 API calls per day")
    print("   • Current weather data")
    print("   • 5-day forecasts")
    print("   • Weather for any city worldwide")
    
    api_key = input("\n🔑 Enter your OpenWeatherMap API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting...")
        return None
    
    # Save to environment for this session
    os.environ["OPENWEATHER_API_KEY"] = api_key
    
    print(f"✅ API key set for this session: {api_key[:8]}...")
    print("\n💡 To make this permanent, add this to your shell profile:")
    print(f"export OPENWEATHER_API_KEY='{api_key}'")
    
    return api_key

async def test_api():
    """Test the API with a sample request."""
    print("\n🧪 Testing API connection...")
    
    try:
        # Import and test the server
        sys.path.append('/Users/naveenvivek/VSCode/MCPserver')
        from international_weather_server import get_current_weather, get_api_status
        
        # Test API status
        status = await get_api_status()
        print(f"Status: {status}")
        
        if "✅" in status:
            print("\n🌤️  Testing weather for Singapore...")
            singapore_weather = await get_current_weather("Singapore", "SG")
            print(singapore_weather)
            
            print("\n🗽 Testing weather for New York...")
            ny_weather = await get_current_weather("New York", "US")
            print(ny_weather)
            
            return True
        else:
            print("❌ API test failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def create_env_file():
    """Create a .env file for the API key."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("❌ No API key found")
        return
    
    env_file = "/Users/naveenvivek/VSCode/MCPserver/.env"
    with open(env_file, "w") as f:
        f.write(f"OPENWEATHER_API_KEY={api_key}\n")
    
    print(f"✅ Created .env file: {env_file}")

def show_usage_examples():
    """Show example usage of the weather server."""
    print("\n🌍 International Weather Server Usage Examples:")
    print("=" * 50)
    
    examples = [
        ("Singapore weather", "get_current_weather('Singapore', 'SG')"),
        ("London forecast", "get_weather_forecast('London', 'UK')"),
        ("Tokyo by coordinates", "get_weather_by_coordinates(35.6762, 139.6503)"),
        ("Search cities", "search_cities('San Francisco')"),
        ("Paris weather", "get_current_weather('Paris', 'FR')"),
    ]
    
    for desc, code in examples:
        print(f"📋 {desc}: {code}")

async def main():
    """Main setup function."""
    try:
        # Setup API key
        api_key = setup_api_key()
        if not api_key:
            return
        
        # Test the API
        if await test_api():
            print("\n🎉 Setup completed successfully!")
            
            # Create .env file
            create_env_file()
            
            # Show usage examples
            show_usage_examples()
            
            print("\n🚀 Next steps:")
            print("1. Add the server to Claude Desktop configuration")
            print("2. Test with queries like 'What's the weather in Singapore?'")
            print("3. Try forecast queries like 'Weather forecast for Tokyo'")
            
        else:
            print("\n❌ Setup failed. Please check your API key and try again.")
            
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled.")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
