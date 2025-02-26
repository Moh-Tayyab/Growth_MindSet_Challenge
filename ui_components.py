import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.express as px
from datetime import datetime
import requests
import pandas as pd
import config  # Ensure this module exists with API keys and defaults

# Note: Create a config.py file with:
# OPENWEATHER_API_KEY = "your_api_key"
# DEFAULT_LAT = 51.5074  # e.g., London
# DEFAULT_LON = -0.1278
# DEFAULT_ZOOM = 10

def setup_page_config():
    """Configure page settings with enhanced theme support"""
    st.set_page_config(
        page_title="Weather Wizard Pro",
        page_icon="🌐",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # Initialize theme in session state
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    # Theme switching in sidebar
    with st.sidebar:
        st.title("🎨 Theme Settings")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌞 Light", key="light_btn"):
                st.session_state.theme = "light"
        with col2:
            if st.button("🌙 Dark", key="dark_btn"):
                st.session_state.theme = "dark"
    
    # CSS for consistent styling across themes
    common_style = """
        <style>
            .main {padding: 2rem 1rem;}
            .stButton>button {
                border-radius: 8px; 
                transition: all 0.3s ease; 
                font-weight: 500;
                padding: 0.5rem 1rem;
            }
            .stAlert {border-radius: 10px; padding: 1rem;}
            .metric-box {
                padding: 1rem; 
                border-radius: 12px; 
                margin: 0.5rem 0; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .weather-card {
                border-radius: 15px; 
                padding: 1.5rem; 
                margin: 1rem 0; 
                transition: transform 0.2s ease;
            }
            .weather-card:hover {transform: translateY(-5px);}
        </style>
    """
    
    dark_style = """
        <style>
            body {color: #ffffff; font-family: 'Segoe UI', sans-serif;}
            .stApp {background: linear-gradient(135deg, #1e2529 0%, #2c353d 100%);}
            .stSidebar {background: #252c33; border-right: 1px solid #3a444e;}
            .stButton>button {
                background: #3a444e; 
                color: #ffffff; 
                border: 1px solid #4a5663;
            }
            .metric-box {background: #2d353d; border: 1px solid #3a444e;}
            .weather-card {background: #2d353d; border: 1px solid #3a444e;}
            p, span, label, .stMarkdown, .stText, h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
            }
            .stTextInput>div>input {
                background: #252c33; 
                color: #ffffff; 
                border: 1px solid #3a444e;
            }
            [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
                color: #ffffff !important;
            }
            .stProgress > div {background-color: #4a5663;}
        </style>
    """
    
    light_style = """
        <style>
            body {color: #2d3436; font-family: 'Segoe UI', sans-serif;}
            .stApp {background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);}
            .stSidebar {background: #ffffff; border-right: 1px solid #e0e0e0;}
            .stButton>button {
                background: #ffffff; 
                color: #2d3436; 
                border: 1px solid #d0d0d0;
            }
            .stButton>button:hover {
                background: #f0f0f0; 
                color: #1a1a1a; 
                border-color: #b0b0b0;
            }
            .metric-box {background: #ffffff; border: 1px solid #e0e0e0;}
            .weather-card {background: #ffffff; border: 1px solid #e0e0e0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);}
            .stTextInput>div>input {
                background: #ffffff; 
                color: #2d3436; 
                border: 1px solid #d0d0d0;
                border-radius: 8px;
            }
        </style>
    """
    
    st.markdown(common_style, unsafe_allow_html=True)
    st.markdown(dark_style if st.session_state.theme == "dark" else light_style, unsafe_allow_html=True)

def render_current_weather(weather_data, units):
    """Display current weather with responsive layout"""
    temp_unit = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{weather_data['name']}, {weather_data['sys']['country']}**")
        st.markdown(f"{weather_data['weather'][0]['description'].title()}")
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Temperature", f"{weather_data['main']['temp']}{temp_unit}")
            st.metric("Humidity", f"{weather_data['main']['humidity']}%")
        with metric_col2:
            st.metric("Feels Like", f"{weather_data['main']['feels_like']}{temp_unit}")
            st.metric("Wind Speed", f"{weather_data['wind']['speed']} {speed_unit}")
    with col2:
        icon_url = f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@4x.png"
        st.image(icon_url, width=150)

def process_forecast_data(data, units):
    """Process forecast data into a 5-day structured DataFrame"""
    daily_data = {}
    for item in data['list']:
        dt = datetime.fromtimestamp(item['dt']).date()
        if dt not in daily_data:
            daily_data[dt] = {'temps': [], 'humidity': [], 'wind_speed': [], 'icons': []}
        daily_data[dt]['temps'].append(item['main']['temp'])
        daily_data[dt]['humidity'].append(item['main']['humidity'])
        daily_data[dt]['wind_speed'].append(item['wind']['speed'])
        daily_data[dt]['icons'].append(item['weather'][0]['icon'])
    
    processed = []
    for date, values in daily_data.items():
        processed.append({
            'date': date,
            'max_temp': max(values['temps']),
            'min_temp': min(values['temps']),
            'avg_humidity': sum(values['humidity']) / len(values['humidity']),
            'avg_wind': sum(values['wind_speed']) / len(values['wind_speed']),
            'icon': max(set(values['icons']), key=values['icons'].count),
            'wind_unit': 'm/s' if units == 'metric' else 'mph'
        })
    
    processed.sort(key=lambda x: x['date'])
    df = pd.DataFrame(processed[:5])
    df['date_str'] = df['date'].apply(lambda x: x.strftime('%a, %b %d'))
    return df

def render_forecast(forecast_data, units):
    """Display interactive 5-day forecast"""
    df = process_forecast_data(forecast_data, units)
    
    with st.container():
        st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
        st.subheader("5-Day Weather Forecast")
        
        tab1, tab2 = st.tabs(["Temperature Chart", "Daily Details"])
        
        with tab1:
            template = 'plotly_dark' if st.session_state.theme == 'dark' else 'plotly_white'
            fig = px.line(df, x='date', y=['max_temp', 'min_temp'],
                          labels={'value': f'Temperature ({units})', 'variable': 'Temperature'},
                          title='Temperature Trends', template=template)
            fig.update_layout(
                hovermode='x unified',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=60, l=40, r=40, b=40)
            )
            fig.update_traces(line=dict(width=3, color='#ff7f0e'), name='Max Temp', selector=dict(name='max_temp'))
            fig.update_traces(line=dict(width=3, color='#1f77b4'), name='Min Temp', selector=dict(name='min_temp'))
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            cols = st.columns(5)
            for idx, row in df.iterrows():
                with cols[idx]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 10px; 
                                background-color: {'#2d353d' if st.session_state.theme == 'dark' else '#f8f9fa'}; 
                                border: 1px solid {'#3a444e' if st.session_state.theme == 'dark' else '#e0e0e0'}; 
                                height: 100%;">
                        <h4>{row['date_str']}</h4>
                        <img src="http://openweathermap.org/img/wn/{row['icon']}@2x.png" style="width: 64px; height: 64px;">
                        <div><span style="font-size: 1.1rem; font-weight: bold; color: #ff7f0e;">{row['max_temp']}°</span> / 
                             <span style="font-size: 1.1rem; font-weight: bold; color: #1f77b4;">{row['min_temp']}°</span></div>
                        <div style="color: {'#e0e0e0' if st.session_state.theme == 'dark' else '#666'};">💧 {int(row['avg_humidity'])}%</div>
                        <div style="color: {'#e0e0e0' if st.session_state.theme == 'dark' else '#666'};">🌬️ {row['avg_wind']:.1f} {row['wind_unit']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_map():
    """Interactive map with theme-aware tiles and search"""
    with st.container():
        
        #st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
        #st.subheader("Interactive Location Selection")
        st.markdown("""
        <div class="weather-card">
            <h4 style = "font-size:2.1rem">Interactive Location Selection</h>
        """, unsafe_allow_html=True)
        
        search_query = st.text_input("🔍 Search location:", placeholder="Enter city, state, or country", key="map_search")
        
        tiles = 'cartodbdark_matter' if st.session_state.theme == "dark" else 'cartodbpositron'
       # m = folium.Map(location=[config.DEFAULT_LAT, config.DEFAULT_LON], zoom_start=config.DEFAULT_ZOOM, tiles=tiles)
        m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)  # Default: London
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if search_query:
            try:
                url = "http://api.openweathermap.org/geo/1.0/direct"
                params = {"q": search_query, "limit": 5, "appid": config.OPENWEATHER_API_KEY}
                response = requests.get(url, params=params)
                if response.status_code != 200:
                    st.error("Failed to fetch location data. Check your API key or connection.")
                else:
                    locations = response.json()
                    if locations:
                        for loc in locations:
                            folium.Marker(
                                [loc['lat'], loc['lon']],
                                popup=f"{loc.get('name', '')}, {loc.get('state', '')}, {loc.get('country', '')}",
                                icon=folium.Icon(color='red', icon='info-sign')
                            ).add_to(m)
                        m.location = [locations[0]['lat'], locations[0]['lon']]
                        m.zoom_start = 10
                    else:
                        st.warning("No locations found. Try a different search term.")
            except requests.exceptions.RequestException as e:
                st.error(f"Network error during search: {str(e)}")
        
        folium.plugins.Fullscreen().add_to(m)
        folium.plugins.MousePosition().add_to(m)
        folium.plugins.Draw(export=True, position='topleft', 
                            draw_options={'polyline': False, 'rectangle': False, 'polygon': False, 'circle': False}).add_to(m)
        
        folium_static(m, width=800, height=500)
        st.markdown("</div>", unsafe_allow_html=True)

def main():
    setup_page_config()
    
    with st.sidebar:
        st.title("⚙️ Settings")
        units = st.selectbox("Measurement Units", ["Metric", "Imperial"])
        st.info("Select location via map or search above")
    
    st.title("🌦️ Weather Wizard Pro")
    
    search_col, _ = st.columns([2, 1])
    with search_col:
        location = st.text_input("Enter Location:", placeholder="Search city or coordinates...")
    
    if location:
        try:
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units={units.lower()}&appid={config.OPENWEATHER_API_KEY}"
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&units={units.lower()}&appid={config.OPENWEATHER_API_KEY}"
            
            weather_response = requests.get(weather_url)
            forecast_response = requests.get(forecast_url)
            
            weather_data = weather_response.json()
            forecast_data = forecast_response.json()
            
            if weather_response.status_code != 200:
                st.error(f"Weather error: {weather_data.get('message', 'Unknown error')}")
            elif forecast_response.status_code != 200:
                st.error(f"Forecast error: {forecast_data.get('message', 'Unknown error')}")
            else:
                render_current_weather(weather_data, units.lower())
                render_forecast(forecast_data, units.lower())
        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}")
    
    st.markdown("---")
    render_map()

if __name__ == "__main__":
    main()