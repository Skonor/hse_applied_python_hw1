import streamlit as st
import requests

cities_list = ['Beijing', 'Berlin', 'Cairo', 'Dubai', 'London', 'Los Angeles',
       'Mexico City', 'Moscow', 'Mumbai', 'New York', 'Paris',
       'Rio de Janeiro', 'Singapore', 'Sydney', 'Tokyo']

def get_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['main']['temp']
    elif response.status_code == 401:
        return response.json()['message']
    else:
        return response.status_code

def main():
    st.title('Weather App')

    city = st.selectbox('Select City', cities_list)
    api_key = st.text_input('Enter API Key')
    if st.button('Get Weather'):
        current_weather = get_weather(city, api_key)
        st.write(current_weather)

if __name__ == '__main__':
    main()