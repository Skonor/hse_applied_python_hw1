import requests
import datetime
import asyncio

class WeatherService:
    def __init__(self):
        self.url = 'http://api.openweathermap.org/data/2.5/weather'
        self.cur_weather = None
        self.cur_city = None
        self.timestamp = None
    
    async def fetch_weather(self, city, api_key):
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            self.cur_weather = response.json()['main']['temp']
            self.cur_city = city
            self.timestamp = response.json()['dt']
        elif response.status_code == 401:
            self.cur_weather = response.json()
        
    def get_weather(self):
        return self.cur_weather, self.cur_city
    
    def get_season(self):
        date = datetime.datetime.fromtimestamp(self.timestamp)
        month = date.month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'