# weather_utils.py
import requests
import os
from dotenv import load_dotenv

# Load environment variables
if os.path.exists('.streamlit/secrets.toml'):
    load_dotenv('.streamlit/secrets.toml')

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_weather_data(city, unit_system='metric'):
    """Fetch current weather data for a given city."""
    if not OPENWEATHER_API_KEY:
        raise ValueError("API key is not set")
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': unit_system
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Could not fetch weather data for {city}: {response.status_code}")

def get_forecast_data(city, unit_system='metric'):
    """Fetch 5-day forecast data for a given city."""
    if not OPENWEATHER_API_KEY:
        raise ValueError("API key is not set")
    
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': unit_system
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Could not fetch forecast data for {city}: {response.status_code}")