import os
from dotenv import load_dotenv
import streamlit as st

# Load .env file if it exists (for local development)
if os.path.exists(".env"):
    load_dotenv()

# Attempt to load API key from Streamlit secrets first
try:
    OPENWEATHER_API_KEY = st.secrets["openweather"]["OPENWEATHER_API_KEY"]
except KeyError:
    # Fallback to environment variable if not in secrets
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not OPENWEATHER_API_KEY:
        raise ValueError("OpenWeather API key not found. Please set it in Streamlit secrets or as an environment variable.")

# API Configuration
BASE_URL = "http://api.openweathermap.org/data/2.5"

# Map Configuration
DEFAULT_LAT = 51.5074
DEFAULT_LON = -0.1278
DEFAULT_ZOOM = 10