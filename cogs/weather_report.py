import pyowm
import os
from dotenv import load_dotenv
from discord.ext import commands


class WeatherReport(commands.Cog):
    load_dotenv()
    apikey = os.getenv('WEATHER')
    owm = pyowm.OWM(apikey)
    mgr = owm.weather_manager()

    def __init__(self, client):
        self.client = client

    def mphToKmph(self, mph):
        kmph = (float)(mph * 1.60934)
        kmph = str(round(kmph, 2))
        return kmph

    @commands.command()
    async def weather(self, ctx, loc):
        location = self.mgr.weather_at_place(loc)
        weather = location.weather
        temp = weather.temperature('celsius')['temp']
        humidity = weather.humidity
        wind_speed = weather.wind(unit='miles_hour')['speed']
        wind = self.mphToKmph(wind_speed)
        rain = weather.rain
        status = weather.detailed_status
        await ctx.send(f"Location:\t{location.location.name}\n"
                       f"Temperature:\t{temp} °C\n"
                       f"Humidity:\t{humidity} %\n"
                       f"Wind:\t{wind} km/h\n"
                       f"Status:\t{status}")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            message = "Not so fast! You need to introduce a city"
        elif isinstance(error, commands.CommandInvokeError):
            message = "We couldn't identify the city :("
        else:
            raise error
        await ctx.send(message)
        await ctx.message.delete(delay=5)


def setup(client):
    client.add_cog(WeatherReport(client))
