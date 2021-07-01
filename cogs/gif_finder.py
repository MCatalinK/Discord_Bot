import os

import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands


class GifFinder(commands.Cog):
    load_dotenv()
    GifToken = os.getenv('GIF')

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gif(self, ctx, keyword):
        search_term = keyword
        request = requests.get("https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, self.GifToken, 1))
        data = request.json()
        embed = discord.Embed(title=keyword,
                              colour=discord.Colour.green())
        embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(GifFinder(client))
