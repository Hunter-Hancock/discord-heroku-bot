import discord
from discord.ext import commands
import datetime as dt

class Presence(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, oldMember, newMember):
        if oldMember.status != newMember.status:
            sendDM()

    @staticmethod
    async def sendDM():
        me = self.client.get_user('102817191446982656')
        
        hr = dt.datetime.today().hour
        if hr > 12 and hr < 24:
            (await me).send('test')

def setup(client):
    client.add_cog(Presence(client))