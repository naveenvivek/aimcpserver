#!/usr/bin/env python3
"""
International Weather MCP Server

A Model Context Protocol server that provides global weather information using OpenWeatherMap API.
This server exposes tools for getting weather data from any city worldwide.

Features:
- Current weather for any city globally
- Weather forecasts for any location
- Weather alerts/warnings (where available)
- Support for coordinates or city names
"""

from typing import Any, Dict, Optional
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("international-weather")

# Constants
OPENWEATHER_API_BASE = "https://api.openweathermap.org/data/2.5"
OPENWEATHER_ONECALL_BASE = "https://api.openweathermap.org/data/3.0"
USER_AGENT = "international-weather-mcp/1.0"

# You'll need to get a free API key from https://openweathermap.org/api
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

async def make_weather_request(url: str, params: Dict[str, Any]) -> Dict[str, Any] | None:
    """Make a request to OpenWeatherMap API with proper error handling."""
    if not API_KEY:
        print("❌ OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY environment variable.")
        return None
    
    headers = {
        "User-Agent": USER_AGENT
    }
    
    # Add API key to parameters
    params["appid"] = API_KEY
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making weather request: {e}")
            return None

def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return round(kelvin - 273.15, 1)

def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    return round((kelvin - 273.15) * 9/5 + 32, 1)

def format_current_weather(data: Dict[str, Any], city: str) -> str:
    """Format current weather data into a readable string."""
    if not data:
        return f"Unable to fetch weather data for {city}"
    
    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    wind = data.get("wind", {})
    clouds = data.get("clouds", {})
    
    temp_k = main.get("temp", 0)
    feels_like_k = main.get("feels_like", 0)
    temp_min_k = main.get("temp_min", 0)
    temp_max_k = main.get("temp_max", 0)
    
    return f"""
🌤️ Current Weather in {city}:

🌡️  Temperature: {kelvin_to_celsius(temp_k)}°C ({kelvin_to_fahrenheit(temp_k)}°F)
🤔 Feels like: {kelvin_to_celsius(feels_like_k)}°C ({kelvin_to_fahrenheit(feels_like_k)}°F)
📊 Min/Max: {kelvin_to_celsius(temp_min_k)}°C / {kelvin_to_celsius(temp_max_k)}°C

☁️  Conditions: {weather.get('main', 'Unknown')} - {weather.get('description', 'No description')}
💨 Wind: {wind.get('speed', 0)} m/s from {wind.get('deg', 0)}°
💧 Humidity: {main.get('humidity', 0)}%
🌫️  Clouds: {clouds.get('all', 0)}%
🔽 Pressure: {main.get('pressure', 0)} hPa
👁️  Visibility: {data.get('visibility', 'N/A')} meters
"""

def format_forecast(data: Dict[str, Any], city: str) -> str:
    """Format 5-day forecast data into a readable string."""
    if not data or "list" not in data:
        return f"Unable to fetch forecast data for {city}"
    
    forecast_list = data["list"][:8]  # Get next 8 periods (24 hours worth)
    
    forecasts = []
    for item in forecast_list:
        dt = item.get("dt_txt", "Unknown time")
        main = item.get("main", {})
        weather = item.get("weather", [{}])[0]
        wind = item.get("wind", {})
        
        temp_k = main.get("temp", 0)
        
        forecast = f"""
📅 {dt}:
🌡️  {kelvin_to_celsius(temp_k)}°C ({kelvin_to_fahrenheit(temp_k)}°F)
☁️  {weather.get('main', 'Unknown')} - {weather.get('description', '')}
💨 Wind: {wind.get('speed', 0)} m/s
💧 Humidity: {main.get('humidity', 0)}%
"""
        forecasts.append(forecast)
    
    return f"🌍 24-Hour Forecast for {city}:\n" + "\n---".join(forecasts)

async def get_coordinates_from_city(city: str, country: str = "") -> tuple[float, float] | None:
    """Get coordinates for a city using OpenWeatherMap geocoding."""
    url = "http://api.openweathermap.org/geo/1.0/direct"
    query = f"{city},{country}" if country else city
    
    params = {
        "q": query,
        "limit": 1
    }
    
    data = await make_weather_request(url, params)
    
    if data and len(data) > 0:
        location = data[0]
        return location.get("lat"), location.get("lon")
    
    return None

@mcp.tool()
async def get_current_weather(city: str, country: str = "") -> str:
    """Get current weather for any city worldwide.

    Args:
        city: Name of the city (e.g., "Singapore", "London", "New York")
        country: Optional country code or name (e.g., "SG", "UK", "US")
    """
    url = f"{OPENWEATHER_API_BASE}/weather"
    
    # Build query string
    query = f"{city},{country}" if country else city
    
    params = {
        "q": query
    }
    
    data = await make_weather_request(url, params)
    return format_current_weather(data, f"{city}, {country}" if country else city)

@mcp.tool()
async def get_weather_by_coordinates(latitude: float, longitude: float) -> str:
    """Get current weather for specific coordinates.

    Args:
        latitude: Latitude of the location (-90 to 90)
        longitude: Longitude of the location (-180 to 180)
    """
    url = f"{OPENWEATHER_API_BASE}/weather"
    
    params = {
        "lat": latitude,
        "lon": longitude
    }
    
    data = await make_weather_request(url, params)
    return format_current_weather(data, f"Coordinates {latitude}, {longitude}")

@mcp.tool()
async def get_weather_forecast(city: str, country: str = "") -> str:
    """Get 5-day weather forecast for any city worldwide.

    Args:
        city: Name of the city (e.g., "Singapore", "London", "New York") 
        country: Optional country code or name (e.g., "SG", "UK", "US")
    """
    url = f"{OPENWEATHER_API_BASE}/forecast"
    
    # Build query string
    query = f"{city},{country}" if country else city
    
    params = {
        "q": query
    }
    
    data = await make_weather_request(url, params)
    return format_forecast(data, f"{city}, {country}" if country else city)

@mcp.tool()
async def get_forecast_by_coordinates(latitude: float, longitude: float) -> str:
    """Get 5-day weather forecast for specific coordinates.

    Args:
        latitude: Latitude of the location (-90 to 90)
        longitude: Longitude of the location (-180 to 180)
    """
    url = f"{OPENWEATHER_API_BASE}/forecast"
    
    params = {
        "lat": latitude,
        "lon": longitude
    }
    
    data = await make_weather_request(url, params)
    return format_forecast(data, f"Coordinates {latitude}, {longitude}")

@mcp.tool()
async def search_cities(query: str) -> str:
    """Search for cities by name to get their exact names and coordinates.

    Args:
        query: City name to search for (e.g., "Singapore", "San Francisco")
    """
    url = "http://api.openweathermap.org/geo/1.0/direct"
    
    params = {
        "q": query,
        "limit": 5
    }
    
    data = await make_weather_request(url, params)
    
    if not data:
        return f"No cities found matching '{query}'"
    
    results = []
    for location in data:
        name = location.get("name", "Unknown")
        country = location.get("country", "Unknown")
        state = location.get("state", "")
        lat = location.get("lat", 0)
        lon = location.get("lon", 0)
        
        location_str = f"{name}, {state}, {country}" if state else f"{name}, {country}"
        results.append(f"📍 {location_str} ({lat}, {lon})")
    
    return f"🔍 Cities matching '{query}':\n\n" + "\n".join(results)

@mcp.tool()
async def get_api_status() -> str:
    """Check if the OpenWeatherMap API is accessible and properly configured."""
    if not API_KEY:
        return "❌ No API key configured. Please set OPENWEATHER_API_KEY environment variable."
    
    # Test with a simple request to London
    url = f"{OPENWEATHER_API_BASE}/weather"
    params = {"q": "London,UK"}
    
    data = await make_weather_request(url, params)
    
    if data:
        return "✅ OpenWeatherMap API is working correctly!"
    else:
        return "❌ OpenWeatherMap API is not responding. Check your API key and internet connection."

if __name__ == "__main__":
    print("🌍 International Weather MCP Server")
    print("Make sure to set OPENWEATHER_API_KEY environment variable!")
    print("Get your free API key at: https://openweathermap.org/api")
    
    # Initialize and run the server
    mcp.run(transport='stdio')
