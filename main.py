import discord
import os

from discord.ext import commands
from Functionality.WeatherConfiguration import WeatherConfiguration
from Functionality.GifConfiguration import GifConfiguration
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD')
prefix = '.'

client = discord.Client()
bot = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}!')


@client.event
async def on_member_join(member):
    server = member.guild

    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, we are glad to have you on {server}!'
    )


@client.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user:
        return

    if msg.startswith('hello' or 'hey'):
        await message.channel.send(f'Hello {message.author.mention}! I hope your day is going great! ^^')

    if msg.startswith('.weather'):
        location = msg.split(".weather ", 1)[1]
        if location is None:
            await message.channel.send("You need to introduce a city!")
        try:
            weather = WeatherConfiguration(location)
            await message.channel.send(weather)
        except:
            await message.channel.send("We couldn't identify the city!")

    if msg.startswith('.gif'):
        search_term = msg.split('.gif ', 1)[1]
        gifs = GifConfiguration(search_term)
        try:
            gif_url = gifs.get_gif()
            embed = discord.Embed(title=search_term)
            embed.set_image(url=gif_url)
            await message.channel.send(embed=embed)
        except:
            await message.channel.send("We couldn't find the gif")


client.run(TOKEN)
