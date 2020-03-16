import discord
from discord.ext import commands, tasks
from itertools import cycle
from mcstatus import MinecraftServer

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # @commands.Cog.listener()
    # async def on_ready(self):
    #    self.update_status.start()

    @commands.command()
    async def status(self, ctx, ip: str):
        try:
            server = MinecraftServer.lookup(ip)
            status = server.status()
            await ctx.send(status.players.online)
        except Exception as e:
            print(e)
        
    # @tasks.loop(seconds=5)
    # async def update_status(self):
    #     server = MinecraftServer.lookup('68.63.192.222:25565')
    #     status = server.status()
    #     await client.change_presence(activity=discord.Game(f'{status.players.online}/5 players on server'))

def setup(client):
    client.add_cog(Status(client))