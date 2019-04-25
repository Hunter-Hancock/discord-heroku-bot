import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
bot = Bot(command_prefix='!')



@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='NO AVENGERS SPOILERS!'))

@bot.event
async def on_message(message):
    message_content = message.content.strip().lower()
    if any(spoiler in message_content for spoiler in spoiler_text):
        await bot.send_message(message.channel, 'No spoilers bud')
        await bot.delete_message(message)
