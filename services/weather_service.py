import requests
import datetime
import asyncio
import aiohttp

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
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    self.cur_weather = data['main']['temp']
                    self.cur_city = city
                    self.timestamp = data['dt']
                elif response.status == 401:
                    self.cur_weather = await response.json()
        
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