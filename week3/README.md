A Model Context Protocol (MCP) server that provides weather information using the OpenWeatherMap API. This server exposes two tools: (1) getting weather conditions, adn (2) getting weather forecasts. 

- **Current Weather**: Get real-time weather conditions for any city
- **Weather Forecast**: Get 1-5 day weather forecasts with detailed information

## Prerequisites
- Python 3.8 or higher
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

## Environment Setup
### 1. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 2. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap API](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Copy your API key

### 3. Configure Environment

Create a `.env` file in the `server` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
OPENWEATHER_API_KEY=your_actual_api_key_here
```

### 4. Test the Server

Run the server to test it:

```bash
cd server
python main.py
```

The server should start and wait for MCP client connections via STDIO.

## MCP Client Configuration

### Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/absolute/path/to/week3/server/main.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Replace `/absolute/path/to/week3/server/main.py` with the actual path to your `main.py` file.

## Tool Reference

### 1. get_current_weather

Get current weather conditions for a specific location.

**Parameters:**
- `location` (string, required): City name, state code, and country code
  - Examples: "London,UK", "New York,NY,US", "Tokyo,JP"

**Example Usage:**
```
What's the current weather in London?
```

**Example Output:**
```
Current weather in London, GB:
🌡️ Temperature: 15.2°C (feels like 14.8°C)
☁️ Conditions: Partly cloudy
💧 Humidity: 78%
🌬️ Wind: 3.2 m/s
📊 Pressure: 1013 hPa
👁️ Visibility: 10.0 km
```

### 2. get_forecast

Get weather forecast for a specific location.

**Parameters:**
- `location` (string, required): City name, state code, and country code
- `days` (integer, optional): Number of days to forecast (1-5, default: 5)

**Example Usage:**
```
What's the 3-day forecast for New York?
```

**Example Output:**
```
5-day weather forecast for New York, US:

📅 2024-01-15:
   🌡️ 8.5°C - 12.3°C
   ☁️ Clear sky
   💧 65% humidity
   🌬️ 2.1 m/s wind

📅 2024-01-16:
   🌡️ 6.2°C - 10.8°C
   ☁️ Few clouds
   💧 72% humidity
   🌬️ 3.5 m/s wind

📅 2024-01-17:
   🌡️ 4.1°C - 9.2°C
   ☁️ Light rain
   💧 85% humidity
   🌬️ 4.2 m/s wind
```

## Error Handling

The server includes comprehensive error handling for:

- **Invalid API Key**: Returns clear error message
- **Location Not Found**: Handles 404 errors gracefully
- **Rate Limiting**: Detects and reports API rate limit exceeded
- **Network Timeouts**: 10-second timeout with clear error messages
- **Invalid Parameters**: Validates input parameters and provides helpful error messages

## API Rate Limits

OpenWeatherMap free tier includes:
- 1,000 calls per day
- 60 calls per minute

The server respects these limits and will return appropriate error messages when limits are exceeded.

## Development

### Project Structure

```
server/
├── main.py              # MCP server entry point
├── tools.py             # Weather API tools and logic
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── __init__.py          # Package initialization
```

### Adding New Tools

To add new weather-related tools:

1. Add the function to `tools.py`
2. Add the tool definition to the `TOOLS` list
3. Add the handler in `main.py`'s `call_tool` function

### Testing

Test individual functions:

```python
import asyncio
from tools import get_current_weather, get_forecast

async def test():
    weather = await get_current_weather("London,UK")
    print(weather)
    
    forecast = await get_forecast("New York,NY,US", 3)
    print(forecast)

asyncio.run(test())
```

## Troubleshooting

### Common Issues

1. **"OPENWEATHER_API_KEY environment variable is required"**
   - Make sure you've set the API key in your `.env` file or environment

2. **"Invalid API key"**
   - Verify your API key is correct and active
   - Check that you've copied the full key without extra spaces

3. **"Location not found"**
   - Try using the format "City,Country" (e.g., "London,UK")
   - Use ISO country codes for better results

4. **"API rate limit exceeded"**
   - Wait a minute before making more requests
   - Consider upgrading to a paid OpenWeatherMap plan

### Debug Mode

Enable debug logging by setting the log level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is for educational purposes as part of the Modern Software Development course.

## API Integration Details

### External API: OpenWeatherMap
- **Provider**: [OpenWeatherMap](https://openweathermap.org/)
- **API Version**: 2.5
- **Authentication**: API Key (free tier: 1,000 calls/day, 60 calls/minute)
- **Rate Limits**: Handled with graceful error messages

### Endpoints Used

#### 1. Current Weather Endpoint
- **URL**: `https://api.openweathermap.org/data/2.5/weather`
- **Method**: GET
- **Parameters**:
  - `q`: Location (city,state,country)
  - `appid`: API key
  - `units`: metric (Celsius)
- **Response**: Real-time weather data including temperature, humidity, pressure, wind, visibility

#### 2. Forecast Endpoint
- **URL**: `https://api.openweathermap.org/data/2.5/forecast`
- **Method**: GET
- **Parameters**:
  - `q`: Location (city,state,country)
  - `appid`: API key
  - `units`: metric (Celsius)
- **Response**: 5-day weather forecast with 3-hour intervals

### Data Processing
- Converts API responses to user-friendly format with emojis
- Groups forecast data by day for daily summaries
- Handles missing data fields gracefully
- Provides temperature ranges and average conditions

## Deployment Modes

### Local STDIO Server (Implemented)
- **Transport**: STDIO (stdin/stdout)
- **Client Integration**: Claude Desktop, Cursor IDE
- **Configuration**: JSON config file
- **Advantages**: Simple setup, no network exposure, direct integration

## Authentication Implementation

### API Key Authentication (Implemented)
- **Method**: Environment variable configuration
- **Security**: Keys stored in environment, not in code
- **Client Config**: API key passed through MCP client configuration
- **Validation**: Server validates API key before making requests

## Example Invocation Flows

### Claude Desktop Integration
1. **User asks**: "What's the weather in London?"
2. **Claude detects**: Weather-related query
3. **Claude calls**: `get_current_weather` tool with `{"location": "London,UK"}`
4. **Server processes**: API request to OpenWeatherMap
5. **Server returns**: Formatted weather data
6. **Claude responds**: Weather information with emojis

### MCP Inspector Testing
1. **Open**: `http://localhost:6274`
2. **Select tool**: `get_current_weather`
3. **Enter parameters**: `{"location": "Tokyo,JP"}`
4. **Click**: "Call Tool"
5. **View result**: Formatted weather response

### Cursor IDE Integration
1. **Configure**: MCP server in Cursor settings
2. **Ask AI**: "What's the 3-day forecast for Paris?"
3. **AI uses**: `get_forecast` tool automatically
4. **Receive**: Detailed forecast information

## API Attribution

Weather data provided by [OpenWeatherMap](https://openweathermap.org/).
