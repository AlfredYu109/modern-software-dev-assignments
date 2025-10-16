# week3/server/tools.py
import os
import logging
import asyncio
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field
from mcp import Tool
from mcp.types import TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenWeatherMap API configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

class WeatherData(BaseModel):
    """Weather data model"""
    temperature: float = Field(description="Temperature in Celsius")
    feels_like: float = Field(description="Feels like temperature in Celsius")
    humidity: int = Field(description="Humidity percentage")
    pressure: int = Field(description="Atmospheric pressure in hPa")
    description: str = Field(description="Weather description")
    wind_speed: float = Field(description="Wind speed in m/s")
    visibility: Optional[int] = Field(description="Visibility in meters")

class ForecastData(BaseModel):
    """Forecast data model"""
    date: str = Field(description="Date of forecast")
    temperature_max: float = Field(description="Maximum temperature in Celsius")
    temperature_min: float = Field(description="Minimum temperature in Celsius")
    description: str = Field(description="Weather description")
    humidity: int = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in m/s")

async def make_api_request(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make HTTP request with error handling and rate limiting"""
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY environment variable is required")
    
    params["appid"] = API_KEY
    params["units"] = "metric"  # Use Celsius
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid API key")
            elif e.response.status_code == 429:
                raise ValueError("API rate limit exceeded. Please try again later.")
            elif e.response.status_code == 404:
                raise ValueError("Location not found")
            else:
                raise ValueError(f"API request failed: {e.response.status_code}")
        except httpx.TimeoutException:
            raise ValueError("API request timed out")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise ValueError("Failed to fetch weather data")

async def get_current_weather(location: str) -> str:
    """
    Get current weather for a specific location.
    
    Args:
        location: City name, state code, and country code (e.g., "London,UK" or "New York,NY,US")
    
    Returns:
        Current weather information as a formatted string
    """
    try:
        url = f"{BASE_URL}/weather"
        params = {"q": location}
        
        data = await make_api_request(url, params)
        
        weather = WeatherData(
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            description=data["weather"][0]["description"],
            wind_speed=data["wind"]["speed"],
            visibility=data.get("visibility")
        )
        
        result = f"""Current weather in {data['name']}, {data['sys']['country']}:
🌡️ Temperature: {weather.temperature:.1f}°C (feels like {weather.feels_like:.1f}°C)
☁️ Conditions: {weather.description.title()}
💧 Humidity: {weather.humidity}%
🌬️ Wind: {weather.wind_speed} m/s
📊 Pressure: {weather.pressure} hPa"""
        
        if weather.visibility:
            result += f"\n👁️ Visibility: {weather.visibility/1000:.1f} km"
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting current weather: {e}")
        return f"Error: {str(e)}"

async def get_forecast(location: str, days: int = 5) -> str:
    """
    Get weather forecast for a specific location.
    
    Args:
        location: City name, state code, and country code (e.g., "London,UK" or "New York,NY,US")
        days: Number of days to forecast (1-5, default: 5)
    
    Returns:
        Weather forecast information as a formatted string
    """
    try:
        if days < 1 or days > 5:
            return "Error: Forecast days must be between 1 and 5"
        
        url = f"{BASE_URL}/forecast"
        params = {"q": location}
        
        data = await make_api_request(url, params)
        
        # Group forecasts by date and get daily summaries
        daily_forecasts = {}
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    "temps": [],
                    "descriptions": [],
                    "humidity": [],
                    "wind_speed": []
                }
            
            daily_forecasts[date]["temps"].append(item["main"]["temp"])
            daily_forecasts[date]["descriptions"].append(item["weather"][0]["description"])
            daily_forecasts[date]["humidity"].append(item["main"]["humidity"])
            daily_forecasts[date]["wind_speed"].append(item["wind"]["speed"])
        
        # Take only the requested number of days
        forecast_days = list(daily_forecasts.keys())[:days]
        
        result = f"5-day weather forecast for {data['city']['name']}, {data['city']['country']}:\n\n"
        
        for date in forecast_days:
            day_data = daily_forecasts[date]
            temp_max = max(day_data["temps"])
            temp_min = min(day_data["temps"])
            avg_humidity = sum(day_data["humidity"]) // len(day_data["humidity"])
            avg_wind = sum(day_data["wind_speed"]) / len(day_data["wind_speed"])
            
            # Get most common description
            description = max(set(day_data["descriptions"]), key=day_data["descriptions"].count)
            
            result += f"📅 {date}:\n"
            result += f"   🌡️ {temp_min:.1f}°C - {temp_max:.1f}°C\n"
            result += f"   ☁️ {description.title()}\n"
            result += f"   💧 {avg_humidity}% humidity\n"
            result += f"   🌬️ {avg_wind:.1f} m/s wind\n\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting forecast: {e}")
        return f"Error: {str(e)}"

#Tool defns for MCP
TOOLS = [
    Tool(
        name="get_current_weather",
        description="Get current weather conditions for a specific location",
        inputSchema={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, state code, and country code (e.g., 'London,UK' or 'New York,NY,US')"
                }
            },
            "required": ["location"]
        }
    ),
    Tool(
        name="get_forecast",
        description="Get weather forecast for a specific location",
        inputSchema={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, state code, and country code (e.g., 'London,UK' or 'New York,NY,US')"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to forecast (1-5, default: 5)",
                    "minimum": 1,
                    "maximum": 5,
                    "default": 5
                }
            },
            "required": ["location"]
        }
    )
]