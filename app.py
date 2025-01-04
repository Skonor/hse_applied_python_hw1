import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import asyncio

from services.weather_service import WeatherService
from services.historical_storage_service import HistoricalStorageService
async def main():
    if 'historical_storage_service' not in st.session_state:
        st.session_state.historical_storage_service = HistoricalStorageService()
    
    if 'weather_service' not in st.session_state: 
        st.session_state.weather_service = WeatherService()

    if 'city' not in st.session_state: 
        st.session_state.city = None

    st.title('Weather App')

    historical_weather = st.file_uploader('Upload Historical Weather Data', type=['csv'])  
    if historical_weather is not None:
        historical_data = pd.read_csv(historical_weather)
        st.session_state.historical_storage_service.fetch_data(historical_data)
        await st.session_state.historical_storage_service.analyze_data()  
        city = st.selectbox('Select City', st.session_state.historical_storage_service.get_cities_list())
        api_key = st.text_input('Enter API Key')
        if st.button('Get Weather Statistics'):
            st.session_state.city = city
        if st.session_state.city is not None:
            fig = st.session_state.historical_storage_service.plot_data(st.session_state.city)
            st.pyplot(fig)
            seasonal_stats = st.session_state.historical_storage_service.get_seasonal_stats(st.session_state.city)
            st.write(seasonal_stats)

        if st.button('Get Current Weather'):
           await st.session_state.weather_service.fetch_weather(city, api_key)
        
        current_weather, current_city = st.session_state.weather_service.get_weather()
        if isinstance(current_weather, float):
            st.write(f'The current temperature in {current_city} is {current_weather}°C')
            current_season = st.session_state.weather_service.get_season()
            is_anomaly = st.session_state.historical_storage_service.is_anomaly(current_city, current_season, current_weather)
            if is_anomaly:
                st.write('This temperature is an anomaly')
            else:
                st.write('This temperature is not an anomaly')
        elif isinstance(current_weather, dict):
            st.write(current_weather)

if __name__ == '__main__':
    asyncio.run(main())