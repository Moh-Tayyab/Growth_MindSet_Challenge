from typing import Dict, Any, Optional
import requests
import streamlit as st
from datetime import datetime
import config

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_weather_data(city: str, units: str = "metric") -> Optional[Dict[str, Any]]:
    """Get current weather data for a city"""
    try:
        response = requests.get(
            f"{config.BASE_URL}/weather",
            params={
                "q": city,
                "units": units,
                "appid": config.OPENWEATHER_API_KEY
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

@st.cache_data(ttl=300)
def get_forecast_data(city, units="metric"):
    """Fetch 5-day forecast data for a given city"""
    try:
        url = f"{config.BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": config.OPENWEATHER_API_KEY,
            "units": units
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {str(e)}")
        return None 