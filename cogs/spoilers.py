import discord
from discord.ext import commands

class Spoilers(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        spoiler_list = ['avengers', 'endgame', 'iron man', 'dies', 'captain america', 'ant man', 'thanos', 'avengers endgame', 'thor', 'black panther', 'spider-man']

        global global_message
        global_message = message

        [item.lower() for item in spoiler_list]

        message_content = message.content.strip().lower()
        if any(spoiler in message_content for spoiler in spoiler_list):
            if 'fortnite' in message_content or message_content.startswith('--'):
                pass
            else:
                await message.channel.purge(limit=1)
                await message.channel.send('No spoilers bud!')
                

def setup(client):
    client.add_cog(Spoilers(client))