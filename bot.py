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
    await client.change_presence(game=discord.Game(name='!gif, !imgur 24/7 Gif bot'))
    print('Ready')

@client.command(pass_context=True)
async def imgur(ctx, *args):

    search = '+'.join(str(i) for i in args)
    res = [item for item in  imgclient.gallery_search(search, sort='top', window='all')]

    if (len(res) == 0):
        await client.say('Sorry no results for: %s' % search)
    else:
        await client.say('Here is what i found for: %s on imgur' % search)
        await client.say(res[random.randint(0, len(res))].link)

# @client.command(pass_context=True)
# async def join(ctx):
#     channel = ctx.message.author.voice.voice_channel
#     await client.join_voice_channel(channel)

# @client.command(pass_context=True)
# async def leave(ctx):
#     server = ctx.message.server
#     voice_client = client.voice_client_in(server)
#     await voice_client.disconnect()

@client.command(pass_context=True)
async def patch(ctx):
    reddit = praw.Reddit(user_agent='discord-bot (by /u/MildlyAdequateDOC)',
                    client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                    username='MildlyAdequateDOC', password=os.environ.get('REDDIT_PASSWORD'))

    posts = []

    for post in reddit.subreddit('blackops4').hot():
        posts.append(post)

    embed = discord.Embed(
        title = posts[1].title,
        colour = discord.Colour.green())
    embed.set_footer(text=posts[1].url)

    await client.say('Here is the latest patch notes for Black ops 4.')
    await client.say(embed=embed)

@client.command(pass_context=True)
async def reddit(ctx, *args):
    reddit = praw.Reddit(user_agent='discord-bot (by /u/MildlyAdequateDOC)',
                    client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                    username='MildlyAdequateDOC', password=os.environ.get('REDDIT_PASSWORD'))
    q = ''.join(str(i) for i in args)
    posts = []

    length = len(posts) - 1

    for post in reddit.subreddit(q).hot():
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

        r = requests.get('https://api.gfycat.com/v1/me/gfycats/search?search_text=%s' % q)
        data = r.json()

        k = 0
        while k < len(data):
            urls.append(data['gfycats'][k]['mp4Url'])
            k += 1

        i = 0
        while i < len(api_response.data):
            urls.append(api_response.data[i].images.original.url)
            urls.append(api_response2.data[i].images.original.url)
            i += 1
        
        if (len(urls) == 0):
            await client.say('Sorry no results for: %s' % q)
        else:
            await client.say('Here is what i found for: %s on giphy/gfycat' % q)
            await client.say(urls[random.randint(0, len(urls) - 1)])
        
    except discord.ClientException as e:
        await client.say(e)

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

async def summon(self, ctx):
    """Summons the bot to join your voice channel."""
    summoned_channel = ctx.message.author.voice_channel
    if summoned_channel is None:
        await self.bot.say('You are not in a voice channel.')
        return False

    state = self.get_voice_state(ctx.message.server)
    if state.voice is None:
        state.voice = await self.bot.join_voice_channel(summoned_channel)
    else:
        await state.voice.move_to(summoned_channel)

    return True

@client.command(pass_context=True, no_pm=True)
async def play(self, ctx, *, song : str):
    """Plays a song.
    If there is a song currently in the queue, then it is
    queued until the next song is done playing.
    This command automatically searches as well from YouTube.
    The list of supported sites can be found here:
    https://rg3.github.io/youtube-dl/supportedsites.html
    """

    state = self.get_voice_state(ctx.message.server)
    opts = {
        'default_search': 'auto',
        'quiet': True,
    }

    if state.voice is None:
        success = await ctx.invoke(self.summon)
        if not success:
            return

    try:
        player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
    except Exception as e:
        fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
        await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
    else:
        player.volume = 0.6
        entry = VoiceEntry(ctx.message, player)
        await self.bot.say('Enqueued ' + str(entry))
        await state.songs.put(entry)

@client.command(pass_context=True, no_pm=True)
async def stop(self, ctx):
    """Stops playing audio and leaves the voice channel.
    This also clears the queue.
    """
    server = ctx.message.server
    state = self.get_voice_state(server)

    if state.is_playing():
        player = state.player
        player.stop()

    try:
        state.audio_player.cancel()
        del self.voice_states[server.id]
        await state.voice.disconnect()
    except:
        pass

@client.command(pass_context=True, no_pm=True)
async def skip(self, ctx):
    state = self.get_voice_state(ctx.message.server)
    if not state.is_playing():
        await self.bot.say('Not playing any music right now...')
        return

    voter = ctx.message.author
    if voter == state.current.requester:
        await self.bot.say('Requester requested skipping song...')
        state.skip()
    elif voter.id not in state.skip_votes:
        state.skip_votes.add(voter.id)
        total_votes = len(state.skip_votes)
        if total_votes >= 3:
            await self.bot.say('Skip vote passed, skipping song...')
            state.skip()
        else:
            await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
    else:
        await self.bot.say('You have already voted to skip this song.')

client.run(os.environ.get('BOT_TOKEN'))