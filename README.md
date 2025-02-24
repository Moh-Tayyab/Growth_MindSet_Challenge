# Weather Wizard 🌦️

A professional weather dashboard built with Streamlit that provides real-time weather data and forecasts using the OpenWeatherMap API.

![Weather Wizard Demo](demo.gif)

## Features 🌟

- **Real-time Weather Data**: Get current weather conditions for any location
- **5-Day Forecast**: View detailed weather forecasts with interactive charts
- **Interactive Map**: Search locations using an interactive map interface
- **Dual Search Methods**: Search by city name or map selection
- **Responsive Design**: Works on desktop and mobile devices
- **Dark/Light Mode**: Toggle between dark and light themes
- **Unit Conversion**: Switch between metric and imperial units

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-wizard.git
   cd weather-wizard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenWeatherMap API key:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure 📁

```
weather-wizard/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── ui_components.py    # UI components and layouts
├── weather_utils.py    # Weather data utilities
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (not tracked)
└── README.md          # Project documentation
```

## Technologies Used 💻

- [Streamlit](https://streamlit.io/) - Web application framework
- [OpenWeatherMap API](https://openweathermap.org/api) - Weather data provider
- [Plotly](https://plotly.com/) - Interactive charts
- [Folium](https://python-visualization.github.io/folium/) - Interactive maps
- [Pandas](https://pandas.pydata.org/) - Data manipulation

## Configuration ⚙️

The application can be configured through environment variables:

- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key
- Default map coordinates can be modified in `config.py`

## Features in Detail 📝

### Current Weather
- Temperature
- Humidity
- Wind Speed
- Weather Description
- Weather Icon

### 5-Day Forecast
- Daily Temperature Range
- Weather Conditions
- Humidity Levels
- Wind Speed
- Interactive Temperature Chart

### Map Features
- Location Search
- Interactive Markers
- Fullscreen Mode
- Mouse Position Tracking
- Drawing Tools

## Contributing 🤝

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- OpenWeatherMap for providing the weather data API
- Streamlit team for the amazing framework
- All contributors who help improve this project

## Contact 📧

Muhammad Tayyab - [your-email@example.com](mailto:your-email@example.com)

Project Link: [https://github.com/your-github-username/weather-wizard](https://github.com/your-github-username/weather-wizard)

---
Made with ❤️ by Muhammad Tayyab

