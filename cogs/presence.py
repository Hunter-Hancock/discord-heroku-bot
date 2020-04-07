import discord
from discord.ext import commands, tasks
import datetime as dt

class Presence(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def check_online(self, ctx):
        me = self.client.get_user(102817191446982656)

    @commands.Cog.listener()
    async def on_member_update(self, oldMember, newMember):
        if oldMember.status != newMember.status:
            await self.sendDM(oldMember, newMember)

    async def sendDM(self, oldMember, newMember):
        channel = self.client.get_channel(225748465714462721)

        server = self.client.get_guild(225748465714462721)

        role = discord.utils.find(lambda r: r.name == 'WEEB', server.roles)

        hr = dt.datetime.today().hour
        if role in newMember.roles:
            if (hr > 12 and hr < 24) and (str(newMember.status) == 'online'):
                await channel.send(f'{newMember.name} is {newMember.status} :green_circle:')

def setup(client):
    client.add_cog(Presence(client))