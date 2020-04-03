import discord
from discord.ext import commands

class Presence(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    def on_member_update(self, oldMember, newMember):
        
        print(f'{oldMember.name} is now {newMember.status}')

def setup(client):
    client.add_cog(Presence(client))