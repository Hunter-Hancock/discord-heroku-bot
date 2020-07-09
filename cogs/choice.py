import discord
from discord.ext import commands
import random

class Choice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def choice(self, ctx, *message):
        options = ' '.join(str(i) for i in message)
        await ctx.send(random.choice(options.split(' | ')))

def setup(client):
    client.add_cog(Choice(client))