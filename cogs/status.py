import discord
from discord.ext import commands, tasks
from itertools import cycle
from mcstatus import MinecraftServer

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.task_status.start()

    @commands.command()
    async def status(self, ctx, ip: str, mode: str):
        server = MinecraftServer.lookup(ip)
        if mode == 'status':
            try:
                status = server.status()
                await ctx.send(status.players.online)
            except Exception as e:
                print(e)
        elif mode == 'ping':
            await ctx.send(server.ping)
        elif mode == 'query':
            query = server.query()
            await ctx.send(', '.join(query.players.names) + 'is on the server' )
        
    @tasks.loop(seconds=10)
    async def task_status(self):
        try:
            server = MinecraftServer.lookup('68.63.192.222')
            status = server.status()
            players = status.players.online
            statuses = cycle(['!gif !imgur !reddit !nsfw', f'Enigmatica 2 Expert: {players}/4'])
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(next(statuses)))
        except Exception:
            statuses = cycle(['!gif !imgur !reddit !nsfw', 'Minecraft Server offline'])
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(next(statuses)))

    @commands.command()
    async def update_status(self, ctx, *option: str):
        server = MinecraftServer.lookup('68.63.192.222')
        status = server.status()
        players = status.players.players
        if option:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(''.join(option)))
        else:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'Enigmatica 2 Expert: {players}/4'))

    @task_status.before_loop
    async def before_update_status(self):
        print('waiting...')
        await self.client.wait_until_ready()
        
def setup(client):
    client.add_cog(Status(client))