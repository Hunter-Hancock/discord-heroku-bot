import discord
from discord.ext import commands, tasks
from itertools import cycle
from mcstatus import MinecraftServer

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.update_status.start()
        print('Ready 2')

    @commands.command()
    async def status(self, ctx, ip: str, mode: str):
        if mode == 'status':
            try:
                server = MinecraftServer.lookup(ip)
                status = server.status()
                await ctx.send(status.players.online)
            except Exception as e:
                print(e)
        elif mode == 'ping':
            await ctx.send(server.ping)
        elif mode == 'query':
            query = server.query()
            await ctx.send(', '.join(query.players.names) + 'is on the server' )
        
    @tasks.loop(seconds=30)
    async def update_status(self):
        server = MinecraftServer.lookup('68.63.192.222')
        status = server.status()
        statuses = ['!gif !imgur !reddit !nsfw', f'Enigmatica 2 Expert: {status.players.online}/4 players on server']
        await client.change_presence(status=discord.Status.online, activity=discord.Game(next(statuses)))
        print('Changed Status')
        
        
def setup(client):
    client.add_cog(Status(client))