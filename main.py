import discord
import os

from discord.ext import commands
from discord.ext.commands import has_permissions
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD')

client = commands.Bot(command_prefix='.', case_insensitive=True)
client.remove_command('help')


@client.command()
@has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
@has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

client.run(TOKEN)
