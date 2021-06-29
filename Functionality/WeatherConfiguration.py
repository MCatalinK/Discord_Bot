import pyowm
import os
from dotenv import load_dotenv


class WeatherConfiguration:
    load_dotenv()
    # apikey = '7084aa2af8f66051b35364db8b84aaee'
    apikey = os.getenv('WEATHER')
    owm = pyowm.OWM(apikey)
    mgr = owm.weather_manager()

    def __init__(self, location):
        self.location = self.mgr.weather_at_place(location)

        if self.location is None:
            self.location = None
            return

        self.weather = self.location.weather
        self.temp = self.weather.temperature('celsius')['temp']
        self.humidity = self.weather.humidity
        self.wind = self.weather.wind(unit='miles_hour')['speed']
        self.rain = self.weather.rain
        self.status = self.weather.detailed_status

    def mphToKmph(self, mph):
        kmph = (float)(mph * 1.60934)
        kmph = str(round(kmph, 2))
        return kmph

    def __str__(self):
        return f"Location:\t{self.location.location.name}\n" \
               f"Temperature:\t{self.temp} °C\n" \
               f"Humidity:\t{self.humidity} %\n" \
               f"Wind:\t{self.mphToKmph(self.wind)} km/h\n" \
               f"Status:\t{self.status}"
