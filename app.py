import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
from datetime import datetime
import plotly.express as px
import pandas as pd
from weather_utils import get_weather_data, get_forecast_data
from ui_components import setup_page_config, render_current_weather, render_map

def main():
    # Setup page configuration and theme
    setup_page_config()
    
    # Sidebar configuration
    with st.sidebar:
        st.title("⚙️ Settings")
        units = st.selectbox(
            "Temperature Units",
            ["Metric (°C)", "Imperial (°F)"],
            help="Choose your preferred temperature unit"
        )
        unit_system = "metric" if "Metric" in units else "imperial"
        
        st.markdown("---")
        st.markdown("### About")
        st.info("Weather Wizard provides real-time weather data and forecasts using the OpenWeatherMap API.")

    # Main content
    st.title("🌦️ Weather Wizard")
    st.markdown("### Your Personal Weather Assistant")
    
    # Search methods
    with st.container():
        search_method = st.radio(
            "Choose search method:",
            ["City Search", "Map Selection"],
            horizontal=True,
            help="Select how you want to search for weather data"
        )
    
    if search_method == "City Search":
        city = st.text_input("Enter city name:", placeholder="e.g., London")
        if city:
            try:
                # Get current weather data
                weather_data = get_weather_data(city, unit_system)
                if weather_data:
                    render_current_weather(weather_data, unit_system)
                    
                    # Get and display forecast data
                    forecast_data = get_forecast_data(city, unit_system)
                    if forecast_data:
                        display_forecast(forecast_data, unit_system)
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    else:  # Map Selection
        render_map()

def process_forecast_data(api_response):
    """Process raw API data into daily aggregated forecast"""
    daily_data = {}
    
    try:
        for item in api_response['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date = dt.strftime('%Y-%m-%d')
            
            if date not in daily_data:
                daily_data[date] = {
                    'temps': [],
                    'humidity': [],
                    'wind_speed': [],
                    'weather_counts': {}
                }
            
            # Aggregate metrics
            daily_data[date]['temps'].append(item['main']['temp'])
            daily_data[date]['humidity'].append(item['main']['humidity'])
            daily_data[date]['wind_speed'].append(item['wind']['speed'])
            
            # Track weather conditions
            weather = item['weather'][0]
            if weather['description'] in daily_data[date]['weather_counts']:
                daily_data[date]['weather_counts'][weather['description']]['count'] += 1
            else:
                daily_data[date]['weather_counts'][weather['description']] = {
                    'count': 1,
                    'icon': weather['icon']
                }

        # Process aggregated data
        processed = []
        for date, data in daily_data.items():
            # Get dominant weather condition
            dominant_weather = max(data['weather_counts'].items(), 
                                key=lambda x: x[1]['count'])
            
            processed.append({
                'date': date,
                'max_temp': max(data['temps']),
                'min_temp': min(data['temps']),
                'avg_humidity': sum(data['humidity'])//len(data['humidity']),
                'avg_wind': round(sum(data['wind_speed'])/len(data['wind_speed']), 1),
                'weather': dominant_weather[0],
                'icon': dominant_weather[1]['icon']
            })
        
        return sorted(processed, key=lambda x: x['date'])[:5]
    
    except Exception as e:
        st.error(f"Data processing error: {str(e)}")
        return []

def display_forecast(forecast_data, unit_system):
    """Display enhanced 5-day forecast with interactive elements"""
    try:
        processed = process_forecast_data(forecast_data)
        if not processed:
            return

        # Unit configuration
        temp_unit = '°C' if unit_system == 'metric' else '°F'
        wind_unit = 'm/s' if unit_system == 'metric' else 'mph'

        # Create temperature chart
        df = pd.DataFrame(processed)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%a, %b %d')
        
        fig = px.line(df, x='date', y=['max_temp', 'min_temp'], 
                    title=f'5-Day Temperature Forecast ({temp_unit})',
                    labels={'value': f'Temperature ({temp_unit})', 'variable': ''},
                    template='plotly_dark')
        
        fig.update_layout(
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            xaxis_title=None,
            yaxis_title=f'Temperature ({temp_unit})',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=20)
        )
        fig.update_traces(
            line=dict(width=2.5),
            selector=dict(name='max_temp'),
            line_color='#FFA500',  # Orange for max temps
            name=''  # Ensure unique name for CSS
        )
        fig.update_traces(
            line=dict(width=2.5),
            selector=dict(name='min_temp'),
            line_color='#1E90FF',  # Dodger blue for min temps
            name=''  # Ensure unique name for CSS
        )
        st.plotly_chart(fig, use_container_width=True)

        # Daily forecast cards
        st.subheader("Detailed Daily Forecast")
        cols = st.columns(5)
        for i, day in enumerate(processed):
            with cols[i]:
                card = st.container()
                with card:
                    # Header with date
                    st.markdown(f"**{pd.to_datetime(day['date']).strftime('%a, %b %d')}**")
                    
                    # Weather icon and condition
                    st.image(f"https://openweathermap.org/img/wn/{day['icon']}@2x.png", 
                           width=80)
                    st.caption(day['weather'].capitalize())
                    
                    # Temperature metrics
                    st.metric("High", f"{day['max_temp']:.1f}{temp_unit}")
                    st.metric("Low", f"{day['min_temp']:.1f}{temp_unit}")
                    
                    # Additional info
                    st.progress(day['avg_humidity']/100, 
                              text=f"💧 Humidity: {day['avg_humidity']}%")
                    st.write(f"🌪️ Wind: {day['avg_wind']} {wind_unit}")
                    
    except Exception as e:
        st.error(f"Forecast display error: {str(e)}")

if __name__ == "__main__":
    main()