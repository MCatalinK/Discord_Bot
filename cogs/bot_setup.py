import discord

from dotenv import load_dotenv
from discord.ext import commands


class BotSetup(commands.Cog):
    load_dotenv()

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged In!")
        await self.client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game(name='Next Gen AI')
        )

    @commands.command()
    async def logout(self):
        await self.client.logout()

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(
            colour=discord.Colour.dark_red()
        )
        embed.set_author(name='Help')
        embed.add_field(
            name='.weather [city/Zipcode]',
            value='It returns the weather of a city of your choice',
            inline=False
        )
        embed.add_field(
            name='.forecast [city/zipcode] [hour]',
            value='It returns the forecast for tomorrow at the specified hour',
            inline=False
        )
        embed.add_field(
            name='.gif [keyword]',
            value='It returns a gif based on a keyword of your choice',
            inline=False
        )
        embed.add_field(
            name='.play [url/keyword]',
            value='Play the specified song.',
            inline=False
        )
        embed.add_field(
            name='.leave',
            value='Kick the bot out of the voice channel',
            inline=False
        )
        embed.add_field(
            name='.pause',
            value='Pause the current playing song',
            inline=False
        )
        embed.add_field(
            name='.resume',
            value='Resume the song.',
            inline=False
        )
        if ctx.message.author.guild_permissions.manage_messages:
            embed.add_field(
                name='.clear [number] //moderator',
                value='Delete the last [number] of messages',
                inline=False
            )

        await ctx.author.send(embed=embed)
        await ctx.message.delete()


def setup(client):
    client.add_cog(BotSetup(client))
