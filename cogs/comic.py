import discord
import requests
import re
from discord.ext import commands

class Comic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def comic(self, ctx, *args):
        p = ' '.join(str(i) for i in args)

        params = self.get_name(p)

        name = params[0].rstrip()

        chapter = params[1]

        for param in params:
            if param == ' ':
                params.remove(param)

        if len(params) > 2:
            try:
                url = f"https://my-comic-api.herokuapp.com/search?name={name.replace(' ', '%20')}&chapter={chapter}"
                print(url)
                response = requests.get(url)

                images = response.json()
                await ctx.send(images['images'][int(params[2])])

            except Exception as e:
                print(e)
                await ctx.send("Couldn't find comic")

        else:
            try:
                url = f"https://my-comic-api.herokuapp.com/search?name={name.replace(' ', '%20')}&chapter={chapter}"
                print(url)
                response = requests.get(url)

                images = response.json()
                # print(images)
                for img in images['images']:
                    await ctx.send(img)

            except Exception as e:
                print(e)
                await ctx.send("Couldn't find comic")

        

    def get_name(self, s):
        return list(filter(None, re.split(r'(\d+)', s)))

def setup(client):
    client.add_cog(Comic(client))