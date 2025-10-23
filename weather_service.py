import requests
import json

class WeatherService:
    def __init__(self):
        # Using free OpenWeatherMap-like API (no key needed for basic info)
        self.base_url = "https://api.openweathermap.org/data/2.5"
        # Fallback to weather search via web
        
    def get_weather_by_location(self, location):
        """Get weather information for a location"""
        try:
            # Try to get weather data via search
            from ddgs import DDGS
            
            weather_query = f"current weather in {location} temperature today"
            
            with DDGS() as ddgs:
                for result in ddgs.text(weather_query, max_results=3):
                    if any(word in result['body'].lower() for word in ['temperature', 'weather', 'celsius', 'fahrenheit']):
                        return self.extract_weather_info(result['body'], location)
            
            return None
            
        except Exception as e:
            print(f"Weather search failed: {e}")
            return None
    
    def extract_weather_info(self, text, location):
        """Extract weather information from search results"""
        import re
        
        # Extract temperature
        temp_match = re.search(r'(\d+)°?[CF]', text)
        temperature = temp_match.group(1) if temp_match else "N/A"
        
        # Extract weather condition
        weather_conditions = ['sunny', 'cloudy', 'rainy', 'stormy', 'clear', 'overcast', 'partly cloudy']
        condition = "N/A"
        for cond in weather_conditions:
            if cond in text.lower():
                condition = cond.title()
                break
        
        return {
            'location': location,
            'temperature': temperature,
            'condition': condition,
            'description': text[:200]
        }
    
    def get_weather_by_pincode(self, pincode, location_finder):
        """Get weather using pincode"""
        try:
            location_info = location_finder.find_location_by_pincode(pincode)
            if location_info:
                location = f"{location_info['area']}, {location_info['district']}, {location_info['state']}"
                return self.get_weather_by_location(location)
            return None
        except:
            return None
    
    def format_weather_response(self, weather_data):
        """Format weather information for display"""
        if not weather_data:
            return "Weather information not available."
        
        response = f"""🌤️ Weather Information:
📍 Location: {weather_data['location']}
🌡️ Temperature: {weather_data['temperature']}°C
☁️ Condition: {weather_data['condition']}

Details: {weather_data['description']}"""
        
        return response
    
    def get_forecast(self, location):
        """Get weather forecast"""
        try:
            from ddgs import DDGS
            
            forecast_query = f"weather forecast {location} next 3 days"
            
            with DDGS() as ddgs:
                for result in ddgs.text(forecast_query, max_results=2):
                    if 'forecast' in result['body'].lower():
                        return result['body'][:300]
            
            return "Forecast not available"
            
        except:
            return "Forecast not available"