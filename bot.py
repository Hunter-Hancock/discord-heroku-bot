import discord
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
import random
import os
from imgurpython import ImgurClient
import requests
import json

client = commands.Bot(command_prefix = '!')

gfyclient_id: '2_WTCi12'
gfyclient_secret: 'J6pITJVLezQShlLJxCqyvxJWOeFklGRepRVE6xvekVmJO69kY8H76HxEipagvA9y'

imgclient_id = os.environ.get('IMGCLIENT_ID')
imgclient_secret = os.environ.get('IMGCLIENT_SECRET')
imgclient = ImgurClient(imgclient_id, imgclient_secret)

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!gif, !imgur 24/7 Gif bot'))
    print('Ready')

@client.command(pass_context=True)
async def imgur(ctx, *args):

    search = '+'.join(str(i) for i in args)
    res = [item for item in  imgclient.gallery_search(search, sort='top', window='all')]

    await client.say('Here is what i found for: %s on imgur' % search)
    await client.say(res[random.randint(0, len(res))].link)

@client.command(pass_context=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)

@client.command(pass_context=True)
async def gif(ctx, *args):
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = os.environ.get('GIF_TOKEN') # str | Giphy API Key.
    q = '+'.join(str(i) for i in args)
    lang = 'en'
    fmt = 'json'

    urls = []

    try: 
        # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, q, limit=100, lang=lang, fmt=fmt)
        
        r = requests.get('https://api.gfycat.com/v1/me/gfycats/search?search_text=%s' % q)
        data = r.json()

        k = 0
        while k < len(data):
            urls.append(data['gfycats'][k]['gifUrl'])
            k += 1

        i = 0
        while i < len(api_response.data):
            urls.append(api_response.data[i].images.original.url)
            i += 1

        await client.say('Here is what i found for: %s on giphy/gfycat' % q)
        await client.say(urls[random.randint(0, len(urls))])
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

client.run(os.environ.get('BOT_TOKEN'))
