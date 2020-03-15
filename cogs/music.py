import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        discord.opus.load_opus()

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

def setup(client):
    client.add_cog(Music(client))