import discord
from discord.ext import commands
import requests
import random
import json

class Gif(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gif(self, ctx, *args):
        q = '+'.join(str(i) for i in args)
        urls = []

        r = requests.get(f'https://api.gfycat.com/v1/me/gfycats/search?search_text={q}&count=250')
        data = r.json()

        length = len(data['gfycats']) - 1
        [urls.append(data['gfycats'][i]['mp4Url']) for i in range(length)]

        await ctx.send(f'Here is what i found for: {q}')
        await ctx.send(urls[random.randint(0, len(urls) - 1)])

def setup(client):
    client.add_cog(Gif(client))