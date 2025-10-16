# Weather MCP Server - Complete Testing Guide

This guide provides step-by-step instructions to test all assignment requirements for the Weather MCP Server.

## 🎯 Assignment Requirements Checklist

### ✅ 1. External API Integration
- **API**: OpenWeatherMap API
- **Endpoints Used**: 
  - `GET /data/2.5/weather` - Current weather data
  - `GET /data/2.5/forecast` - 5-day weather forecast
- **Documentation**: See API endpoints section below

### ✅ 2. Two MCP Tools Exposed
- `get_current_weather` - Real-time weather conditions
- `get_forecast` - 1-5 day weather forecasts

### ✅ 3. Basic Resilience Implementation
- HTTP failure handling
- Timeout handling (10 seconds)
- Rate limit detection
- Input validation
- Graceful error messages

### ✅ 4. Packaging and Documentation
- Clear setup instructions
- Environment variable configuration
- Run commands provided
- Example invocation flows

### ✅ 5. Local STDIO Deployment
- Runs locally via STDIO transport
- Integrates with Claude Desktop
- Discoverable by AI IDEs like Cursor

### ✅ 6. Authentication (Bonus)
- API key support via environment variable
- Secure client configuration

---

## 🧪 Step-by-Step Testing Guide

### **Phase 1: Basic Functionality Testing**

#### Test 1.1: Verify API Integration
```bash
cd /Users/AlfredYu/modern-software-dev-assignments/week3/server
python test_server.py
```

**Expected Output:**
```
Testing Weather MCP Server Functions
==================================================

1. Testing get_current_weather:
Current weather in London, GB:
🌡️ Temperature: 12.4°C (feels like 11.7°C)
☁️ Conditions: Clear Sky
💧 Humidity: 75%
🌬️ Wind: 2.61 m/s
📊 Pressure: 1030 hPa
👁️ Visibility: 10.0 km

2. Testing get_forecast:
5-day weather forecast for New York, US:
📅 2025-10-12:
   🌡️ 8.5°C - 12.3°C
   ☁️ Clear sky
   💧 65% humidity
   🌬️ 2.1 m/s wind
```

**✅ Pass Criteria:** Both tools return formatted weather data

#### Test 1.2: Test MCP Protocol with Inspector
1. Open browser to: `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=c2219c8563bbac9cdb218430374551eb09b7401a2c613a49f3408c2d49ab8f92`
2. You should see two tools listed:
   - `get_current_weather`
   - `get_forecast`
3. Test `get_current_weather`:
   - Click on the tool
   - Enter: `{"location": "Tokyo,JP"}`
   - Click "Call Tool"
   - Verify formatted weather response
4. Test `get_forecast`:
   - Click on the tool
   - Enter: `{"location": "Paris,FR", "days": 3}`
   - Click "Call Tool"
   - Verify 3-day forecast response

**✅ Pass Criteria:** Both tools work in MCP Inspector interface

### **Phase 2: Resilience Testing**

#### Test 2.1: Invalid API Key
```bash
cd /Users/AlfredYu/modern-software-dev-assignments/week3/server
OPENWEATHER_API_KEY=invalid_key python test_server.py
```

**Expected Output:**
```
Error: Invalid API key
```

**✅ Pass Criteria:** Graceful error message, no crash

#### Test 2.2: Invalid Location
In MCP Inspector, test with invalid location:
```json
{"location": "InvalidCity123,XX"}
```

**Expected Output:**
```
Error: Location not found
```

**✅ Pass Criteria:** Clear error message, no crash

#### Test 2.3: Network Timeout Simulation
```bash
# Test with a very short timeout (modify tools.py temporarily)
# Change timeout from 10.0 to 0.1 seconds
```

**Expected Output:**
```
Error: API request timed out
```

**✅ Pass Criteria:** Timeout handling works

#### Test 2.4: Invalid Parameters
In MCP Inspector, test forecast with invalid days:
```json
{"location": "London,UK", "days": 10}
```

**Expected Output:**
```
Error: Forecast days must be between 1 and 5
```

**✅ Pass Criteria:** Input validation works

### **Phase 3: Claude Desktop Integration Testing**

#### Test 3.1: Verify Configuration
```bash
cat ~/Library/Application\ Support/Claude/config.json
```

**Expected Output:**
```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/Users/AlfredYu/modern-software-dev-assignments/week3/server/main.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**✅ Pass Criteria:** MCP server properly configured

#### Test 3.2: Claude Desktop Integration
1. **Restart Claude Desktop** completely
2. **Open new chat**
3. **Test current weather:**
   - Ask: "What's the current weather in Sydney, Australia?"
   - Expected: Claude calls `get_current_weather` and returns formatted data
4. **Test forecast:**
   - Ask: "Give me a 3-day forecast for Berlin, Germany"
   - Expected: Claude calls `get_forecast` and returns 3-day forecast
5. **Test error handling:**
   - Ask: "What's the weather in InvalidCity123?"
   - Expected: Graceful error message

**✅ Pass Criteria:** Claude Desktop successfully uses weather tools

### **Phase 4: Advanced Testing**

#### Test 4.1: Multiple Locations
Test various location formats:
- "London,UK"
- "New York,NY,US"
- "Tokyo,JP"
- "Paris,FR"

**✅ Pass Criteria:** All location formats work

#### Test 4.2: Different Forecast Periods
Test forecast with different day counts:
- 1 day
- 3 days
- 5 days

**✅ Pass Criteria:** All day counts work correctly

#### Test 4.3: Rate Limiting Awareness
Make multiple rapid requests to test rate limit handling.

**✅ Pass Criteria:** Server handles rate limits gracefully

---

## 🔧 Manual Testing Commands

### Test Individual Functions
```python
# Create test_manual.py
import asyncio
from tools import get_current_weather, get_forecast

async def test():
    # Test current weather
    weather = await get_current_weather("London,UK")
    print("Current Weather Test:")
    print(weather)
    print("\n" + "="*50 + "\n")
    
    # Test forecast
    forecast = await get_forecast("New York,NY,US", 3)
    print("Forecast Test:")
    print(forecast)

asyncio.run(test())
```

### Test Error Conditions
```python
# Test with invalid API key
import os
os.environ["OPENWEATHER_API_KEY"] = "invalid"
weather = await get_current_weather("London,UK")
print(weather)  # Should show error message
```

---

## 📊 Success Criteria Summary

| Requirement | Test Method | Pass Criteria |
|-------------|-------------|---------------|
| **External API** | `test_server.py` | Weather data returned |
| **Two MCP Tools** | MCP Inspector | Both tools listed and functional |
| **Error Handling** | Invalid inputs | Graceful error messages |
| **Rate Limiting** | Multiple requests | Proper error handling |
| **Local Deployment** | Claude Desktop | Tools work in chat |
| **Documentation** | README review | Clear setup instructions |
| **Authentication** | Config check | API key properly configured |

---

## 🚨 Troubleshooting

### Common Issues and Solutions

1. **"OPENWEATHER_API_KEY environment variable is required"**
   - Solution: Set API key in `.env` file or environment

2. **"Invalid API key"**
   - Solution: Verify API key is correct and active

3. **"Location not found"**
   - Solution: Use proper format: "City,Country" or "City,State,Country"

4. **MCP Inspector not loading**
   - Solution: Check if port 6274 is available, restart inspector

5. **Claude Desktop not recognizing tools**
   - Solution: Restart Claude Desktop completely, verify config.json

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ✅ Final Verification Checklist

Before submitting, verify:

- [ ] Both weather tools work in MCP Inspector
- [ ] Claude Desktop integration works
- [ ] Error handling works for invalid inputs
- [ ] API key authentication works
- [ ] Documentation is complete and clear
- [ ] All test cases pass
- [ ] Code is clean and well-commented
- [ ] README includes all required information

**🎉 If all items are checked, your Weather MCP Server is ready for submission!**
