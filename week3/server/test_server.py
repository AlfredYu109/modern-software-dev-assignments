#!/usr/bin/env python3
"""
Comprehensive Test Suite for the Weather MCP Server
Tests all functionality, error handling, and edge cases
"""

import asyncio
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our weather functions
from tools import get_current_weather, get_forecast

class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name, passed, error=None):
        self.tests.append({"name": name, "passed": passed, "error": error})
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"📊 TEST SUMMARY: {self.passed} passed, {self.failed} failed")
        print(f"{'='*60}")
        
        for test in self.tests:
            status = "✅ PASS" if test["passed"] else "❌ FAIL"
            print(f"{status}: {test['name']}")
            if test["error"]:
                print(f"    Error: {test['error']}")

async def test_basic_functionality(results):
    """Test basic weather functionality"""
    print("\n🌤️  BASIC FUNCTIONALITY TESTS")
    print("-" * 40)
    
    # Test 1: Current weather - London
    try:
        result = await get_current_weather("London,UK")
        if "Temperature" in result and "London" in result:
            results.add_test("Current weather - London", True)
            print("✅ Current weather (London): PASS")
        else:
            results.add_test("Current weather - London", False, "Invalid response format")
            print("❌ Current weather (London): FAIL - Invalid format")
    except Exception as e:
        results.add_test("Current weather - London", False, str(e))
        print(f"❌ Current weather (London): FAIL - {e}")
    
    # Test 2: Current weather - Tokyo
    try:
        result = await get_current_weather("Tokyo,JP")
        if "Temperature" in result and "Tokyo" in result:
            results.add_test("Current weather - Tokyo", True)
            print("✅ Current weather (Tokyo): PASS")
        else:
            results.add_test("Current weather - Tokyo", False, "Invalid response format")
            print("❌ Current weather (Tokyo): FAIL - Invalid format")
    except Exception as e:
        results.add_test("Current weather - Tokyo", False, str(e))
        print(f"❌ Current weather (Tokyo): FAIL - {e}")
    
    # Test 3: Forecast - 3 days
    try:
        result = await get_forecast("New York,NY,US", 3)
        if "forecast" in result.lower() and "New York" in result:
            results.add_test("Forecast - 3 days", True)
            print("✅ Forecast (3 days): PASS")
        else:
            results.add_test("Forecast - 3 days", False, "Invalid response format")
            print("❌ Forecast (3 days): FAIL - Invalid format")
    except Exception as e:
        results.add_test("Forecast - 3 days", False, str(e))
        print(f"❌ Forecast (3 days): FAIL - {e}")
    
    # Test 4: Forecast - 5 days
    try:
        result = await get_forecast("Paris,FR", 5)
        if "forecast" in result.lower() and "Paris" in result:
            results.add_test("Forecast - 5 days", True)
            print("✅ Forecast (5 days): PASS")
        else:
            results.add_test("Forecast - 5 days", False, "Invalid response format")
            print("❌ Forecast (5 days): FAIL - Invalid format")
    except Exception as e:
        results.add_test("Forecast - 5 days", False, str(e))
        print(f"❌ Forecast (5 days): FAIL - {e}")

async def test_location_formats(results):
    """Test different location formats"""
    print("\n🌍 LOCATION FORMAT TESTS")
    print("-" * 40)
    
    test_locations = [
        ("Sydney,AU", "City,Country"),
        ("San Francisco,CA,US", "City,State,Country"),
        ("Berlin,DE", "City,Country"),
        ("Mumbai,IN", "City,Country"),
        ("São Paulo,BR", "City with special chars,Country")
    ]
    
    for location, format_name in test_locations:
        try:
            result = await get_current_weather(location)
            if "Temperature" in result and not result.startswith("Error"):
                results.add_test(f"Location format: {format_name}", True)
                print(f"✅ {format_name} ({location}): PASS")
            else:
                results.add_test(f"Location format: {format_name}", False, "Invalid response")
                print(f"❌ {format_name} ({location}): FAIL")
        except Exception as e:
            results.add_test(f"Location format: {format_name}", False, str(e))
            print(f"❌ {format_name} ({location}): FAIL - {e}")

async def test_forecast_variations(results):
    """Test different forecast day counts"""
    print("\n📅 FORECAST VARIATION TESTS")
    print("-" * 40)
    
    for days in [1, 2, 3, 4, 5]:
        try:
            result = await get_forecast("London,UK", days)
            if "forecast" in result.lower() and not result.startswith("Error"):
                results.add_test(f"Forecast - {days} day(s)", True)
                print(f"✅ {days} day forecast: PASS")
            else:
                results.add_test(f"Forecast - {days} day(s)", False, "Invalid response")
                print(f"❌ {days} day forecast: FAIL")
        except Exception as e:
            results.add_test(f"Forecast - {days} day(s)", False, str(e))
            print(f"❌ {days} day forecast: FAIL - {e}")

async def test_error_handling(results):
    """Test error handling and edge cases"""
    print("\n⚠️  ERROR HANDLING TESTS")
    print("-" * 40)
    
    # Test 1: Invalid location
    try:
        result = await get_current_weather("InvalidCity123,XX")
        if result.startswith("Error"):
            results.add_test("Invalid location handling", True)
            print("✅ Invalid location: PASS - Error handled")
        else:
            results.add_test("Invalid location handling", False, "Should return error")
            print("❌ Invalid location: FAIL - Should return error")
    except Exception as e:
        results.add_test("Invalid location handling", False, str(e))
        print(f"❌ Invalid location: FAIL - {e}")
    
    # Test 2: Empty location
    try:
        result = await get_current_weather("")
        if result.startswith("Error"):
            results.add_test("Empty location handling", True)
            print("✅ Empty location: PASS - Error handled")
        else:
            results.add_test("Empty location handling", False, "Should return error")
            print("❌ Empty location: FAIL - Should return error")
    except Exception as e:
        results.add_test("Empty location handling", False, str(e))
        print(f"❌ Empty location: FAIL - {e}")
    
    # Test 3: Invalid forecast days (too many)
    try:
        result = await get_forecast("London,UK", 10)
        if "Forecast days must be between 1 and 5" in result:
            results.add_test("Invalid forecast days (too many)", True)
            print("✅ Invalid forecast days (10): PASS - Error handled")
        else:
            results.add_test("Invalid forecast days (too many)", False, "Should return error")
            print("❌ Invalid forecast days (10): FAIL - Should return error")
    except Exception as e:
        results.add_test("Invalid forecast days (too many)", False, str(e))
        print(f"❌ Invalid forecast days (10): FAIL - {e}")
    
    # Test 4: Invalid forecast days (zero)
    try:
        result = await get_forecast("London,UK", 0)
        if "Forecast days must be between 1 and 5" in result:
            results.add_test("Invalid forecast days (zero)", True)
            print("✅ Invalid forecast days (0): PASS - Error handled")
        else:
            results.add_test("Invalid forecast days (zero)", False, "Should return error")
            print("❌ Invalid forecast days (0): FAIL - Should return error")
    except Exception as e:
        results.add_test("Invalid forecast days (zero)", False, str(e))
        print(f"❌ Invalid forecast days (zero): FAIL - {e}")

async def test_response_format(results):
    """Test response format and content"""
    print("\n📋 RESPONSE FORMAT TESTS")
    print("-" * 40)
    
    try:
        result = await get_current_weather("London,UK")
        
        # Check for required elements
        required_elements = ["Temperature", "Humidity", "Wind", "Pressure"]
        missing_elements = []
        
        for element in required_elements:
            if element not in result:
                missing_elements.append(element)
        
        if not missing_elements:
            results.add_test("Response format - required elements", True)
            print("✅ Response format: PASS - All required elements present")
        else:
            results.add_test("Response format - required elements", False, f"Missing: {missing_elements}")
            print(f"❌ Response format: FAIL - Missing elements: {missing_elements}")
        
        # Check for emojis
        emojis = ["🌡️", "☁️", "💧", "🌬️", "📊"]
        emoji_count = sum(1 for emoji in emojis if emoji in result)
        
        if emoji_count >= 3:
            results.add_test("Response format - emojis", True)
            print("✅ Emoji formatting: PASS - Good emoji usage")
        else:
            results.add_test("Response format - emojis", False, f"Only {emoji_count} emojis found")
            print(f"❌ Emoji formatting: FAIL - Only {emoji_count} emojis found")
            
    except Exception as e:
        results.add_test("Response format", False, str(e))
        print(f"❌ Response format: FAIL - {e}")

async def test_performance(results):
    """Test performance and timing"""
    print("\n⚡ PERFORMANCE TESTS")
    print("-" * 40)
    
    # Test response time
    start_time = time.time()
    try:
        result = await get_current_weather("London,UK")
        end_time = time.time()
        response_time = end_time - start_time
        
        if response_time < 5.0:  # Should respond within 5 seconds
            results.add_test("Response time", True)
            print(f"✅ Response time: PASS - {response_time:.2f}s")
        else:
            results.add_test("Response time", False, f"Too slow: {response_time:.2f}s")
            print(f"❌ Response time: FAIL - {response_time:.2f}s (too slow)")
    except Exception as e:
        results.add_test("Response time", False, str(e))
        print(f"❌ Response time: FAIL - {e}")
    
    # Test concurrent requests
    try:
        start_time = time.time()
        tasks = [
            get_current_weather("London,UK"),
            get_current_weather("Paris,FR"),
            get_current_weather("Tokyo,JP")
        ]
        results_concurrent = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        concurrent_time = end_time - start_time
        
        success_count = sum(1 for r in results_concurrent if not isinstance(r, Exception) and not str(r).startswith("Error"))
        
        if success_count >= 2 and concurrent_time < 10.0:
            results.add_test("Concurrent requests", True)
            print(f"✅ Concurrent requests: PASS - {success_count}/3 successful in {concurrent_time:.2f}s")
        else:
            results.add_test("Concurrent requests", False, f"Only {success_count}/3 successful")
            print(f"❌ Concurrent requests: FAIL - Only {success_count}/3 successful")
    except Exception as e:
        results.add_test("Concurrent requests", False, str(e))
        print(f"❌ Concurrent requests: FAIL - {e}")

async def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🧪 COMPREHENSIVE WEATHER MCP SERVER TEST SUITE")
    print("=" * 60)
    
    # Check API key
    if not os.getenv("OPENWEATHER_API_KEY"):
        print("⚠️  WARNING: OPENWEATHER_API_KEY not set!")
        print("   Some tests will fail. Set your API key in .env file.")
        print()
    
    results = TestResults()
    
    # Run all test suites
    await test_basic_functionality(results)
    await test_location_formats(results)
    await test_forecast_variations(results)
    await test_error_handling(results)
    await test_response_format(results)
    await test_performance(results)
    
    # Print summary
    results.print_summary()
    
    # Final verdict
    if results.failed == 0:
        print("\n🎉 ALL TESTS PASSED! Your Weather MCP Server is working perfectly!")
    elif results.failed <= 2:
        print(f"\n✅ MOSTLY WORKING! {results.passed} tests passed, {results.failed} minor issues.")
    else:
        print(f"\n⚠️  NEEDS ATTENTION! {results.failed} tests failed. Check the errors above.")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())
