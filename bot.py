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
    await client.change_presence(game=discord.Game(name='!gif !imgur !reddit 24/7'))
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

@client.command(pass_context=True)
async def patch(ctx):
    reddit = praw.Reddit(user_agent='discord-bot (by /u/MildlyAdequateDOC)',
                    client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                    username='MildlyAdequateDOC', password=os.environ.get('REDDIT_PASSWORD'))

    posts = []

    for post in reddit.subreddit('blackops4').hot():
        if 'Update' in post.title:
            posts.append(post)

    embed = discord.Embed(
        title = posts[0].title,
        colour = discord.Colour.green())
    embed.set_footer(text=posts[0].url)
        


    await client.say('Here is the latest patch notes for Black ops 4.')
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

#music-code:
    # if not discord.opus.is_loaded():
    #     # the 'opus' library here is opus.dll on windows
    #     # or libopus.so on linux in the current directory
    #     # you should replace this with the location the
    #     # opus library is located in and with the proper filename.
    #     # note that on windows this DLL is automatically provided for you
    #     discord.opus.load_opus('opus')

    # class VoiceEntry:
    #     def __init__(self, message, player):
    #         self.requester = message.author
    #         self.channel = message.channel
    #         self.player = player

    #     def __str__(self):
    #         fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
    #         duration = self.player.duration
    #         if duration:
    #             fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
    #         return fmt.format(self.player, self.requester)

    # class VoiceState:
    #     def __init__(self, bot):
    #         self.current = None
    #         self.voice = None
    #         self.bot = bot
    #         self.play_next_song = asyncio.Event()
    #         self.songs = asyncio.Queue()
    #         self.skip_votes = set() # a set of user_ids that voted
    #         self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    #     def is_playing(self):
    #         if self.voice is None or self.current is None:
    #             return False

    #         player = self.current.player
    #         return not player.is_done()

    #     @property
    #     def player(self):
    #         return self.current.player

    #     def skip(self):
    #         self.skip_votes.clear()
    #         if self.is_playing():
    #             self.player.stop()

    #     def toggle_next(self):
    #         self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    #     async def audio_player_task(self):
    #         while True:
    #             self.play_next_song.clear()
    #             self.current = await self.songs.get()
    #             await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
    #             self.current.player.start()
    #             await self.play_next_song.wait()

    # class Music:
    #     """Voice related commands.

    #     Works in multiple servers at once.
    #     """
    #     def __init__(self, bot):
    #         self.bot = bot
    #         self.voice_states = {}

    #     def get_voice_state(self, server):
    #         state = self.voice_states.get(server.id)
    #         if state is None:
    #             state = VoiceState(self.bot)
    #             self.voice_states[server.id] = state

    #         return state

    #     async def create_voice_client(self, channel):
    #         voice = await self.bot.join_voice_channel(channel)
    #         state = self.get_voice_state(channel.server)
    #         state.voice = voice

    #     def __unload(self):
    #         for state in self.voice_states.values():
    #             try:
    #                 state.audio_player.cancel()
    #                 if state.voice:
    #                     self.bot.loop.create_task(state.voice.disconnect())
    #             except:
    #                 pass

    #     @client.command(pass_context=True, no_pm=True)
    #     async def join(self, ctx, *, channel : discord.Channel):
    #         """Joins a voice channel."""
    #         try:
    #             await self.create_voice_client(channel)
    #         except discord.ClientException:
    #             await self.bot.say('Already in a voice channel...')
    #         except discord.ClientException:
    #             await self.bot.say('This is not a voice channel...')
    #         else:
    #             await self.bot.say('Ready to play audio in ' + channel.name)

    #     @client.command(pass_context=True, no_pm=True)
    #     async def summon(self, ctx):
    #         """Summons the bot to join your voice channel."""
    #         summoned_channel = ctx.message.author.voice_channel
    #         if summoned_channel is None:
    #             await self.bot.say('You are not in a voice channel.')
    #             return False

    #         state = self.get_voice_state(ctx.message.server)
    #         if state.voice is None:
    #             state.voice = await self.bot.join_voice_channel(summoned_channel)
    #         else:
    #             await state.voice.move_to(summoned_channel)

    #         return True

    #     @client.command(pass_context=True, no_pm=True)
    #     async def play(self, ctx, *, song : str):
    #         """Plays a song.

    #         If there is a song currently in the queue, then it is
    #         queued until the next song is done playing.

    #         This command automatically searches as well from YouTube.
    #         The list of supported sites can be found here:
    #         https://rg3.github.io/youtube-dl/supportedsites.html
    #         """
    #         state = self.get_voice_state(ctx.message.server)
    #         opts = {
    #             'default_search': 'auto',
    #             'quiet': True,
    #         }

    #         if state.voice is None:
    #             success = await ctx.invoke(self.summon)
    #             if not success:
    #                 return

    #         try:
    #             player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
    #         except Exception as e:
    #             fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
    #             await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
    #         else:
    #             player.volume = 0.6
    #             entry = VoiceEntry(ctx.message, player)
    #             await self.bot.say('Enqueued ' + str(entry))
    #             await state.songs.put(entry)

    #     @client.command(pass_context=True, no_pm=True)
    #     async def volume(self, ctx, value : int):
    #         """Sets the volume of the currently playing song."""

    #         state = self.get_voice_state(ctx.message.server)
    #         if state.is_playing():
    #             player = state.player
    #             player.volume = value / 100
    #             await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    #     @client.command(pass_context=True, no_pm=True)
    #     async def pause(self, ctx):
    #         """Pauses the currently played song."""
    #         state = self.get_voice_state(ctx.message.server)
    #         if state.is_playing():
    #             player = state.player
    #             player.pause()

    #     @client.command(pass_context=True, no_pm=True)
    #     async def resume(self, ctx):
    #         """Resumes the currently played song."""
    #         state = self.get_voice_state(ctx.message.server)
    #         if state.is_playing():
    #             player = state.player
    #             player.resume()

    #     @client.command(pass_context=True, no_pm=True)
    #     async def stop(self, ctx):
    #         """Stops playing audio and leaves the voice channel.

    #         This also clears the queue.
    #         """
    #         server = ctx.message.server
    #         state = self.get_voice_state(server)

    #         if state.is_playing():
    #             player = state.player
    #             player.stop()

    #         try:
    #             state.audio_player.cancel()
    #             del self.voice_states[server.id]
    #             await state.voice.disconnect()
    #         except:
    #             pass

    #     @client.command(pass_context=True, no_pm=True)
    #     async def skip(self, ctx):
    #         """Vote to skip a song. The song requester can automatically skip.

    #         3 skip votes are needed for the song to be skipped.
    #         """

    #         state = self.get_voice_state(ctx.message.server)
    #         if not state.is_playing():
    #             await self.bot.say('Not playing any music right now...')
    #             return

    #         voter = ctx.message.author
    #         if voter == state.current.requester:
    #             await self.bot.say('Requester requested skipping song...')
    #             state.skip()
    #         elif voter.id not in state.skip_votes:
    #             state.skip_votes.add(voter.id)
    #             total_votes = len(state.skip_votes)
    #             if total_votes >= 3:
    #                 await self.bot.say('Skip vote passed, skipping song...')
    #                 state.skip()
    #             else:
    #                 await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
    #         else:
    #             await self.bot.say('You have already voted to skip this song.')

    #     @client.command(pass_context=True, no_pm=True)
    #     async def playing(self, ctx):
    #         """Shows info about the currently played song."""

    #         state = self.get_voice_state(ctx.message.server)
    #         if state.current is None:
    #             await self.bot.say('Not playing anything.')
    #         else:
    #             skip_count = len(state.skip_votes)
    #             await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))

    # bot = client.Bot(command_prefix=client.when_mentioned_or('$'), description='A playlist example for discord.py')
    # bot.add_cog(Music(bot))

client.run(os.environ.get('BOT_TOKEN'))