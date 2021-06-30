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
            name='.weather',
            value='It returns the weather of a city of your choice',
            inline=False
        )
        embed.add_field(
            name='.gif',
            value='It returns a gif based on a keyword of your choice',
            inline=False
        )

        await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(BotSetup(client))
