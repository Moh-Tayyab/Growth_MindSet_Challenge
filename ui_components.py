import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.express as px
from datetime import datetime
import config
import requests
import pandas as pd

def setup_page_config():
    """Configure professional page settings with enhanced theme support"""
    st.set_page_config(
        page_title="Weather Wizard Pro",
        page_icon="🌐",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # Initialize theme with session state
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    # Enhanced theme system in sidebar
    with st.sidebar:
        st.title("🎨 Theme Settings")
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            if st.button("🌞 Light", key="light_btn"):
                st.session_state.theme = "light"
        with theme_col2:
            if st.button("🌙 Dark", key="dark_btn"):
                st.session_state.theme = "dark"
    
    # Professional CSS for both themes
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
            .plot-container {background: transparent !important;}
        </style>
    """
    
    dark_style = """
        <style>
            body {color: #ffffff !important; font-family: 'Segoe UI', sans-serif;}
            .stApp {background: linear-gradient(135deg, #1e2529 0%, #2c353d 100%);}
            .stSidebar {
                background: #252c33 !important; 
                border-right: 1px solid #3a444e;
            }
            .stButton>button {
                background: #3a444e; 
                color: #ffffff !important; 
                border: 1px solid #4a5663;
            }
            .metric-box {
                background: #2d353d; 
                border: 1px solid #3a444e; 
                color: #ffffff !important;
            }
            .weather-card {
                background: #2d353d; 
                border: 1px solid #3a444e;
            }
            /* Ensure all text elements are white in dark mode */
            p, span, label, .stMarkdown, .stText, .metric-container, 
            .stMetric, .stMetricLabel, .stMetricValue {
                color: #ffffff !important;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
            }
            .stTextInput>div>input {
                background: #252c33; 
                color: #ffffff !important; 
                border: 1px solid #3a444e;
            }
            /* Style metrics in dark mode */
            .stMetricValue {
                background-color: #2d353d !important;
                color: #ffffff !important;
            }
            /* Style tabs in dark mode */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #2d353d !important;
            }
            .stTabs [data-baseweb="tab"] {
                color: #ffffff !important;
            }
            /* Style select boxes in dark mode */
            .stSelectbox>div>div {
                background-color: #2d353d !important;
                color: #ffffff !important;
            }
        </style>
    """
    
    light_style = """
        <style>
            body {color: #2d3436; font-family: 'Segoe UI', sans-serif;}
            .stApp {background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);}
            .stSidebar {
                background: #ffffff !important; 
                border-right: 1px solid #e0e0e0;
            }
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
            .metric-box {
                background: #ffffff; 
                border: 1px solid #e0e0e0; 
                color: #2d3436;
            }
            .weather-card {
                background: #ffffff; 
                border: 1px solid #e0e0e0; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            .stTextInput>div>input {
                background: #ffffff; 
                color: #2d3436; 
                border: 1px solid #d0d0d0;
                border-radius: 8px;
            }
        </style>
    """
    
    st.markdown(common_style, unsafe_allow_html=True)
    if st.session_state.theme == "dark":
        st.markdown(dark_style, unsafe_allow_html=True)
    else:
        st.markdown(light_style, unsafe_allow_html=True)

def render_current_weather(weather_data, units):
    """Professional current weather display with responsive layout"""
    temp_unit = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"
    
    # Theme-based colors
    is_dark = st.session_state.theme == "dark"
    text_color = "#ffffff" if is_dark else "#2d3436"
    
    # Global dark mode styles
    st.markdown(f"""
    <style>
        /* Dark mode text colors */
        .dark-theme .stMarkdown, 
        .dark-theme p,
        .dark-theme span,
        .dark-theme h1, .dark-theme h2, .dark-theme h3,
        .dark-theme .stMetric label,
        .dark-theme .stMetric .metric-value {{
            color: {text_color} !important;
        }}
        
        /* Metric styling */
        .dark-theme .stMetric [data-testid="stMetricValue"] {{
            color: {text_color} !important;
        }}
        .dark-theme .stMetric [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}
        
        /* Weather info styling */
        .weather-title {{
            color: {text_color} !important;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}
        .weather-description {{
            color: {text_color} !important;
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Location and description with dark mode classes
        st.markdown(
            f'<div class="weather-title">{weather_data["name"]}, {weather_data["sys"]["country"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="weather-description">{weather_data["weather"][0]["description"].title()}</div>',
            unsafe_allow_html=True
        )
        
        # Weather metrics
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric(
                "Temperature",
                f"{weather_data['main']['temp']}{temp_unit}",
                delta=None,
                help="Current temperature"
            )
            st.metric(
                "Humidity",
                f"{weather_data['main']['humidity']}%",
                delta=None,
                help="Current humidity"
            )
        with metric_col2:
            st.metric(
                "Feels Like",
                f"{weather_data['main']['feels_like']}{temp_unit}",
                delta=None,
                help="Feels like temperature"
            )
            st.metric(
                "Wind Speed",
                f"{weather_data['wind']['speed']} {speed_unit}",
                delta=None,
                help="Current wind speed"
            )
    
    with col2:
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
        st.image(icon_url, width=150)

def render_forecast(forecast_data, units):
    """Interactive professional forecast display"""
    df = process_forecast_data(forecast_data, units)
    
    # Theme-based colors
    text_color = "#ffffff" if st.session_state.theme == "dark" else "#2d3436"
    bg_color = "#2d353d" if st.session_state.theme == "dark" else "#f8f9fa"
    
    with st.container():
        st.markdown(f"""
        <style>
            .dark-mode-forecast {{
                color: {text_color} !important;
                background-color: {bg_color};
            }}
            .dark-mode-forecast .plotly {{
                color: {text_color} !important;
            }}
            .temp-value {{
                color: {text_color} !important;
            }}
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="weather-card">
            <h3 style="margin-bottom: 1.5rem;">5-Day Weather Forecast</h3>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Temperature Chart", "Daily Details"])
        
        with tab1:
            # Create separate traces for max and min temperatures
            fig = px.line(df, x='date', y=['max_temp', 'min_temp'],
                         labels={'value': f'Temperature ({units})',
                                'variable': 'Temperature Range',
                                'date': 'Date'},
                         title='Temperature Trends')
            
            # Update the figure layout and styling
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=text_color,
                title_font_color=text_color,
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(t=60, l=40, r=40, b=40)
            )
            
            # Customize the traces
            fig.update_traces(
                line=dict(width=3, color='#ff7f0e'),
                name='Maximum',
                selector=dict(name='max_temp')
            )
            fig.update_traces(
                line=dict(width=3, color='#1f77b4'),
                name='Minimum',
                selector=dict(name='min_temp')
            )
            
            # Update axes
            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128,128,128,0.2)',
                title_font=dict(size=14)
            )
            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128,128,128,0.2)',
                title_font=dict(size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            cols = st.columns(5)
            for idx, (_, row) in enumerate(df.iterrows()):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="text-align: center; 
                                padding: 1rem; 
                                border-radius: 10px; 
                                background-color: {'#2d353d' if st.session_state.theme == 'dark' else '#f8f9fa'};
                                border: 1px solid {'#3a444e' if st.session_state.theme == 'dark' else '#e0e0e0'};
                                height: 100%;">
                        <h4 style="margin-bottom: 0.5rem;">{row['date']}</h4>
                        <img src="http://openweathermap.org/img/wn/{row['icon']}@2x.png" 
                             style="width: 64px; height: 64px; margin: 0.5rem 0;">
                        <div style="margin: 0.5rem 0;">
                            <span style="font-size: 1.1rem; font-weight: bold; color: #ff7f0e;">
                                {row['max_temp']}°
                            </span>
                            <span style="color: {'#e0e0e0' if st.session_state.theme == 'dark' else '#666'};"> / </span>
                            <span style="font-size: 1.1rem; font-weight: bold; color: #1f77b4;">
                                {row['min_temp']}°
                            </span>
                        </div>
                        <div style="margin: 0.5rem 0; color: {'#e0e0e0' if st.session_state.theme == 'dark' else '#666'};">
                            <div style="margin: 0.3rem 0;">💧 {int(row['humidity'])}%</div>
                            <div style="margin: 0.3rem 0;">🌬️ {row['wind_speed']:.1f} {row['wind_unit']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def process_forecast_data(data, units):
    """Process forecast data into structured DataFrame"""
    processed = []
    wind_unit = 'm/s' if units == 'metric' else 'mph'
    
    for item in data['list']:
        dt = datetime.fromtimestamp(item['dt'])
        entry = {
            'date': dt.strftime('%a, %b %d'),
            'temp': item['main']['temp'],
            'max_temp': item['main']['temp_max'],
            'min_temp': item['main']['temp_min'],
            'humidity': item['main']['humidity'],
            'wind_speed': item['wind']['speed'],
            'description': item['weather'][0]['description'],
            'icon': item['weather'][0]['icon'],
            'wind_unit': wind_unit
        }
        processed.append(entry)
    
    df = pd.DataFrame(processed)
    return df.groupby('date', as_index=False).agg({
        'max_temp': 'max',
        'min_temp': 'min',
        'humidity': 'mean',
        'wind_speed': 'mean',
        'icon': lambda x: x.mode()[0],
        'wind_unit': 'first'
    })

def render_map():
    """Professional interactive map component with search"""
    with st.container():
        st.markdown("""
        <div class="weather-card">
            <h3 style="margin-bottom: 1rem;">Interactive Location Selection</h3>
        """, unsafe_allow_html=True)
        
        # Add search box above map
        search_query = st.text_input("🔍 Search location:", 
                                   placeholder="Enter city, state, or country",
                                   key="map_search")
        
        # Initialize map with light theme only
        m = folium.Map(
            location=[config.DEFAULT_LAT, config.DEFAULT_LON],
            zoom_start=config.DEFAULT_ZOOM,
            tiles='cartodbpositron'  # Light theme only
        )
        
        # Add search functionality
        if search_query:
            try:
                # Geocode the search query
                url = "http://api.openweathermap.org/geo/1.0/direct"
                params = {
                    "q": search_query,
                    "limit": 5,
                    "appid": config.OPENWEATHER_API_KEY
                }
                response = requests.get(url, params=params)
                locations = response.json()
                
                if locations:
                    # Add markers for each found location
                    for loc in locations:
                        folium.Marker(
                            [loc['lat'], loc['lon']],
                            popup=f"{loc.get('name', '')}, {loc.get('state', '')}, {loc.get('country', '')}",
                            icon=folium.Icon(color='red', icon='info-sign')
                        ).add_to(m)
                    
                    # Center map on first result
                    m.location = [locations[0]['lat'], locations[0]['lon']]
                    m.zoom_start = 10
                else:
                    st.warning("Location not found. Please try a different search term.")
            
            except Exception as e:
                st.error(f"Error searching location: {str(e)}")
        
        # Add map controls
        folium.plugins.Fullscreen().add_to(m)
        folium.plugins.MousePosition().add_to(m)
        folium.plugins.Draw(
            export=True,
            position='topleft',
            draw_options={'polyline': False, 'rectangle': False, 'polygon': False, 'circle': False}
        ).add_to(m)
        
        # Display the map
        folium_static(m, width=800, height=500)
        st.markdown("</div>", unsafe_allow_html=True)

def main():
    setup_page_config()
    
    with st.sidebar:
        st.title("⚙️ Settings")
        units = st.selectbox("Measurement Units", ["Metric", "Imperial"])
        st.info("Select location using map or city search above")
    
    st.title("🌦️ Weather Wizard Pro")
    
    search_col, _ = st.columns([2, 1])
    with search_col:
        location = st.text_input("Enter Location:", placeholder="Search city or coordinates...")
    
    if location:
        try:
            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={location}&units={units.lower()}&appid={config.API_KEY}"
            ).json()
            forecast_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={location}&units={units.lower()}&appid={config.API_KEY}"
            ).json()
            
            render_current_weather(weather_data, units.lower())
            render_forecast(forecast_data, units.lower())
            
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
    
    st.markdown("---")
    render_map()

if __name__ == "__main__":
    main()