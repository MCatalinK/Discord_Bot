import discord
import os
import youtube_dl

from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from Functionality.WeatherConfiguration import WeatherConfiguration
from Functionality.GifConfiguration import GifConfiguration
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD')

bot = commands.Bot(command_prefix='.', case_insensitive=True)


@bot.event
async def on_ready():
    print("Logged In!")

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')

    @bot.command()
    async def unload(ctx, extension):
        bot.unload_extension(f'cogs.{extension}')

@bot.command(help="Returns a weather report based on a city.", pass_context=True)
async def weather(ctx, location):
    if location is None:
        await ctx.send("You need to introduce a city!")
    try:
        weather = WeatherConfiguration(location)
        await ctx.send(weather)
    except:
        await ctx.send("We couldn't identify the city!")


@bot.command(help="Returns a gif based on a keyword of your choice.", pass_context=True, )
async def gif(ctx, keyword):
    gifs = GifConfiguration(keyword)
    try:
        gif_url = gifs.get_gif()
        embed = discord.Embed(title=keyword)
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)
    except:
        await ctx.send("We couldn't find the gif")


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)
