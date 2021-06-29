import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


class Moderator(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)


def setup(client):
    client.add_cog(Moderator(client))