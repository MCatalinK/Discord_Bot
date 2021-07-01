import discord.ext.commands
import pyowm
import os
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from pyowm.utils import timestamps


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
    async def weather(self, ctx, *, loc):
        location = self.mgr.weather_at_place(loc)
        weather = location.weather
        temp = weather.temperature('celsius')['temp']
        humidity = weather.humidity
        wind_speed = weather.wind(unit='miles_hour')['speed']
        wind = self.mphToKmph(wind_speed)
        rain = weather.rain
        status = weather.detailed_status

        dt = datetime.now()

        date = dt.strftime("%d.%m.%y")

        await ctx.send(f"**Date:**\t{date}"
                       f"\n**Location:**\t{location.location.name}"
                       f"\n**Temperature:**\t{temp} °C"
                       f"\n**Humidity:**\t{humidity} %"
                       f"\n**Wind:**\t{wind} km/h"
                       f"\n**Status:**\t{status}")

    @weather.error
    async def weather_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            message = "Not so fast! You need to introduce a city"
        elif isinstance(error, commands.CommandInvokeError):
            message = "We couldn't identify the city :("
        elif isinstance(error, commands.UserInputError):
            message = "Something about the input was wrong"
        else:
            raise error
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)

    @commands.command()
    async def forecast(self, ctx, hour: int, *, loc):
        forecast = self.mgr.forecast_at_place(loc, '3h')
        tmr = timestamps.tomorrow(hour, 0)
        weather = forecast.get_weather_at(tmr)
        status = weather.detailed_status
        rain = forecast.will_be_rainy_at(tmr)
        dt = datetime(tmr.year, tmr.month, tmr.day)

        date = dt.strftime("%d.%m.%y")
        await ctx.send(f'**Date:**\t{date}'
                       f'\n**Hour:**\t{hour}:00'
                       f'\n**Status:**\t{status}'
                       f'\n**Will rain:**\t{rain}')

    @forecast.error
    async def forecast_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            message = "The command needs a location and an hour to get the report"
        elif isinstance(error, commands.CommandInvokeError):
            message = "The location or the hour is wrong"
        elif isinstance(error, commands.UserInputError):
            message = "Something about the input was wrong"
        else:
            raise error
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)


def setup(client):
    client.add_cog(WeatherReport(client))
