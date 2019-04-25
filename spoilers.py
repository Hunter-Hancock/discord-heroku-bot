import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
bot = Bot(command_prefix='!')

spoiler_text = ['Avengers', 'Endgame', 'Iron man', 'dies', 'captain america', 'ant man', 'thanos']
@bot.event
async def on_message(message):
    message_content = message.content.stip().lower()
    if any(spoiler in message for spoiler in spoiler_text):
        await bot.send_message(message.channel, 'No spoilers bud')
        await bot.delete_message(message)
bot.run(os.environ.get('BOT_TOKEN'))
