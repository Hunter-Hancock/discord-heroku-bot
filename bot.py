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
import praw
import datetime
import asyncio
import time

client = commands.Bot(command_prefix = '!')

gfyclient_id: '2_WTCi12'
gfyclient_secret: 'J6pITJVLezQShlLJxCqyvxJWOeFklGRepRVE6xvekVmJO69kY8H76HxEipagvA9y'

imgclient_id = os.environ.get('IMGCLIENT_ID')
imgclient_secret = os.environ.get('IMGCLIENT_SECRET')
imgclient = ImgurClient(imgclient_id, imgclient_secret)


#client_auth = requests.auth.HTTPBasicAuth(os.environ.get('REDDIT_CLIENT_ID'), os.environ.get('REDDIT_CLIENT_SECRET'))
#post_data = {"grant_type": "password", "username": "MildlyAdequateDOC", "password": os.environ.get('REDDIT_PASSWORD')}
#headers = {"User-Agent": "discord-bot/0.1 by MildlyAdequateDOC"}
#test_response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
#pprint(test_response.json())

#bot_auth = '112223157440-e_P1wON56ltclGn-2Q2LkSazPwQ' # acquire token

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!gif !imgur !reddit !ffz'))


# now = datetime.datetime.now
# run_at = now + datetime.timedelta(minutes=2)
# if now == run_at:
#     client.send_message(client.get_channel('465986403281534979'), 'Anthem Closed Alpha servers are up.')

# now = datetime.datetime.now()
# run_at = now + datetime.timedelta(hours=11,minutes=5)

# if now == run_at:
#     client.send_message(client.get_channel('225748465714462721'), 'Anthem Closed Alpha servers are up.')



@client.command(pass_context=True)
async def imgur(ctx, *args):

    search = '+'.join(str(i) for i in args)
    res = [item for item in  imgclient.gallery_search(search, sort='top', window='all')]

    if (len(res) == 0):
        await client.say('Sorry no results for: %s' % search)
    else:
        await client.say('Here is what i found for: %s on imgur' % search)
        await client.say(res[random.randint(0, len(res))].link)

@client.command(pass_context=True)
async def patch(ctx, q):
    reddit = praw.Reddit(user_agent='discord-bot (by /u/MildlyAdequateDOC)',
                    client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                    username='MildlyAdequateDOC', password=os.environ.get('REDDIT_PASSWORD'))

    posts = []

    for post in reddit.subreddit(q).hot():
        if 'Update' in post.title:
            posts.append(post)

    embed = discord.Embed(
        title = posts[0].title,
        colour = discord.Colour.green())
    embed.set_footer(text=posts[0].url)

    await client.say('Here is the latest patch notes for %s.' % q)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def reddit(ctx, *args):
    reddit = praw.Reddit(user_agent='discord-bot (by /u/MildlyAdequateDOC)',
                    client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                    username='MildlyAdequateDOC', password=os.environ.get('REDDIT_PASSWORD'))
    q = ''.join(str(i) for i in args)
    posts = []

    for post in reddit.subreddit(q).hot():
        if not post.is_video:
            posts.append(post)

    length = len(posts) - 1

    random.seed(datetime.datetime.now().time())
    wadu = posts[random.randint(0, length)]
    embed = discord.Embed(
        title = wadu.title,
        description = wadu.selftext,
        colour = discord.Colour.green())
    embed.set_image(url=wadu.url)
    embed.set_footer(text='https://www.reddit.com/comments/%s' % wadu.id)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def avatar(ctx):
    user = ctx.message.author
    if not user.avatar_url:
        await client.say(user.avatar_default_url)
    else:
        await client.say(user.avatar_url)

@client.command(pass_context=True)
async def ffz(ctx, q):
    #starttime = time.time()
    if(q == 'monkaS'):
        await client.say('https://cdn.frankerfacez.com/7ed3da04c09547097595ff979e629c36.png')    
    elif(q == None):
        await client.say('Enter an arguement.')
    elif(q == 'hypers'):
        await client.say('https://cdn.frankerfacez.com/2eca1ebdd82e120d31ab3b59e6aea68b.png')
    elif(q == 'pepehands'):
        await client.say('https://cdn.frankerfacez.com/b97ed9ea44a548134578aecd47348784.png')
    else:
        url = 'https://api.frankerfacez.com/v1/emoticons?q=%s&sort=count-desc' % q
        s = requests.Session()
        r = s.get(url).json()
        # r = requests.get(url).json()

    embed = discord.Embed(
        title = q,
        colour = discord.Colour.green())

    try:
        try:
            res = 'https:',(r['emoticons'][0]['urls']['4'])
            embed.set_image(url=''.join(res))
            await client.say(embed=embed)
        except KeyError:
            res = 'https:',(r['emoticons'][0]['urls']['2'])
            embed.set_image(url=''.join(res))
            await client.say(embed=embed)
    except KeyError:
        res = 'https:',(r['emoticons'][0]['urls']['1'])
        embed.set_image(url=''.join(res))
        await client.say(embed=embed)
    #await client.say('Took %s seconds' % round(time.time() - starttime, 2))

    # try:
    #     try:
    #         res = 'https:',(r['emoticons'][0]['urls']['4'])
    #     except KeyError:
    #         res = 'https:',(r['emoticons'][0]['urls']['2'])
    #     await client.say(''.join(res))
    #     await client.say('Took %s seconds' % round(time.time() - starttime, 2))
    # except KeyError:
    #     res = 'https:',(r['emoticons'][0]['urls']['1'])
    #     await client.say(''.join(res))
    #     await client.say('Took %s seconds' % round(time.time() - starttime, 2))


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
        api_response2 = api_instance.gifs_search_get(api_key, q, limit=100, lang=lang, fmt=fmt, offset=100)

        r = requests.get('https://api.gfycat.com/v1/me/gfycats/search?search_text=%s&count=1500' % q)
        data = r.json()

        r2 = requests.get('https://api.tenor.com/v1/search?q=%s' % q)
        data2 = r2.json()

        l = 0
        while l < len(data2['results']):
            urls.append(data2['results'][l]['url'])
            l += 1

        k = 0
        while k < len(data['gfycats']):
            urls.append(data['gfycats'][k]['mp4Url'])
            k += 1

        i = 0
        while i < len(api_response.data):
            urls.append(api_response.data[i].images.original.url)
            urls.append(api_response2.data[i].images.original.url)
            i += 1

        await client.say('Here is what i found for: %s' % q)
        await client.say(urls[random.randint(0, len(urls) - 1)])
        
    except discord.ClientException as e:
        await client.say(e)

client.run(os.environ.get('BOT_TOKEN'))