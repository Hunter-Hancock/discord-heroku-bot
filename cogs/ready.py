import discord
from discord.ext import commands
from .status import Status

class Ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game('!gif !imgur !reddit !nsfw')
        await self.client.change_presence(status=discord.Status.online, activity=game)
        print('Ready')

def setup(client):
    client.add_cog(Ready(client))