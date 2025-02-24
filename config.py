import os
from dotenv import load_dotenv

# Load .env file only in development
if os.path.exists(".env"):
    load_dotenv()

# API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise ValueError("OpenWeather API key not found. Please set OPENWEATHER_API_KEY environment variable.")

BASE_URL = "http://api.openweathermap.org/data/2.5"

# Map Configuration
DEFAULT_LAT = 51.5074
DEFAULT_LON = -0.1278
DEFAULT_ZOOM = 10