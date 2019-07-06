import discord
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException
import random
import os
from imgurpython import ImgurClient
import requests
import praw
import datetime
import time
from twilio.rest import Client
from bs4 import BeautifulSoup
import urllib.request
from googletrans import Translator
from selenium import webdriver

client = commands.Bot(command_prefix='!')

gfyclient_id: '2_WTCi12'
gfyclient_secret: 'J6pITJVLezQShlLJxCqyvxJWOeFklGRepRVE6xvekVmJO69kY8H76HxEipagvA9y'

imgclient_id = os.environ.get('IMGCLIENT_ID')
imgclient_secret = os.environ.get('IMGCLIENT_SECRET')
imgclient = ImgurClient(imgclient_id, imgclient_secret)
translator = Translator()

account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')

# client_auth = requests.auth.HTTPBasicAuth(os.environ.get('REDDIT_CLIENT_ID'), os.environ.get('REDDIT_CLIENT_SECRET'))
# post_data = {"grant_type": "password", "username": "MildlyAdequateDOC", "password": os.environ.get('REDDIT_PASSWORD')}
# headers = {"User-Agent": "discord-bot/0.1 by MildlyAdequateDOC"}
# test_response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
# pprint(test_response.json())

# bot_auth = '112223157440-e_P1wON56ltclGn-2Q2LkSazPwQ' # acquire token

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!gif !imgur !reddit !wfa'))
    # await client.change_presence(game=discord.Game(name='NO SPOILERS!'))

# messages = []

# @client.event
# async def on_message(message):

#     msg = {f"{message.author}: {message.content}"}

#     if message.author.bot or message.content == "!logs": # message.author.id == '102817191446982656':
#         pass
#     else:
#         messages.append(msg)

#     await client.process_commands(message)

# @client.command()
# async def clearlogs():
#     messages.clear()

# @client.command()
# async def logs():
#     await client.say(messages)

# spoiler_list = ['avengers', 'endgame', 'iron man', 'dies', 'captain america', 'ant man', 'thanos', 'avengers endgame', 'thor', 'black panther', 'spider-man']

# [item.lower() for item in spoiler_list]

# @client.event
# async def on_message(message):
#     message_content = message.content.strip().lower()
#     if any(spoiler in message_content for spoiler in spoiler_list):
#         if 'fortnite' in message_content or message_content.startswith('--'):
#             pass
#         else:
#             await client.send_message(message.channel, 'No spoilers bud')
#             await client.delete_message(message)

@client.command(pass_context=True)
async def scrape2(ctx, website, class_name):
    browser = webdriver.Chrome()
    browser.get(website)

    soup = BeautifulSoup(browser.page_source, 'lxml')
    result = soup.find_all('div', class_=class_name)

    urls = []

    for img in result:
        if img.find('img') is not None and img.find('video') == None:
            links = img.find('img')
            urls.append(links['src'])
        else:
            links = img.find('video')
            urls.append(links.source['src'])

    await client.say(urls[random.randint(0, len(urls) - 1)])
    browser.quit()

@client.command(pass_context=True)
async def nsfw(ctx):
    browser = webdriver.Chrome()
    browser.get('https://scrolller.com/')

    nsfw = browser.find_element_by_css_selector('body > div.center-bar > div > div > div:nth-child(2) > a:nth-child(3) > div > div').click()
    women = browser.find_element_by_css_selector('#intro-settings > div > div > div > div:nth-child(3) > div:nth-child(2) > div').click()

    time.sleep(4)

    soup = BeautifulSoup(browser.page_source, 'lxml')
    image = soup.find_all('div', class_=class_name)

    urls = []

    for img in image:
        if img.find('img') is not None and img.find('video') == None:
            links = img.find('img')
            urls.append(links['src'])
        else:
            links = img.find('video')
            urls.append(links.source['src'])

    await client.say(urls[random.randint(0, len(urls) - 1)])
    browser.quit()

@client.command(pass_context=True)
async def snap(ctx):
    channel = ctx.message.channel
    await client.say('SNAP!')
    time.sleep(.5)
    await client.say('https://tenor.com/view/iam-iron-man-iron-man-avengers-endgame-avengers-endgame-gif-14042823')
    async for message in client.logs_from(channel, limit=6):
        time.sleep(7)
        await client.delete_message(message)

@client.command(pass_context=True)
async def imgur(ctx, *args):

    search = '+'.join(str(i) for i in args)
    res = [item for item in imgclient.gallery_search(
        search, sort='top', window='all')]

    if (len(res) == 0):
        await client.say('Sorry no results for: %s' % search)
    else:
        await client.say('Here is what i found for: %s on imgur' % search)
        await client.say(res[random.randint(0, len(res))].link)


@client.command(pass_context=True)
async def translate(ctx, *args):
    imsg = ''.join(str(i) for i in args)
    # tmsg = translator.translate(imsg, dest=lang)
    tmsg = translator.translate(imsg, dest='en')
    # await client.say(f'Translating from {tmsg.src} to {tmsg.dest}')
    await client.say(tmsg.text)

@client.command(pass_context=True)
async def patch(ctx, q):
    reddit = praw.Reddit(user_agent='discord-bot (by /u/MildlyAdequateDOC)',
                         client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                         username='MildlyAdequateDOC', password=os.environ.get('REDDIT_PASSWORD'))

    posts = []

    for post in reddit.subreddit(q).hot():
        if 'Patch' in post.title or 'Patch' in post.selftext:
            posts.append(post)

    embed = discord.Embed(
        title=posts[0].title,
        colour=discord.Colour.green())
    embed.set_footer(text=posts[0].url)

    await client.say('Here is the latest patch notes for %s.' % q)
    # await client.say(embed=embed)
    await client.say(posts[0].url)

    if len(posts) == 0:
        await client.say("Didn't find patch")

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
        title=wadu.title,
        description=wadu.selftext,
        colour=discord.Colour.green())
    embed.set_image(url=wadu.url)
    embed.set_footer(text='https://www.reddit.com/comments/%s' % wadu.id)
    await client.say(embed=embed)
    await client.say('https://www.reddit.com/comments/%s' % wadu.id)

@client.command(pass_context=True)
async def avatar(ctx):
    user = ctx.message.author
    if user.avatar == None:
        await client.say('https://cdn.discordapp.com/embed/avatars/0.png')
    else:
        await client.say(user.avatar_url)

@client.command()
async def tomatoes(*args):
    text = []
    q = '_'.join(str(i) for i in args)
    r = requests.get(f'https://www.rottentomatoes.com/m/{q}')
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
    for i in soup.find_all('span', class_='mop-ratings-wrap__percentage'):
        text.append(i.text)
    await client.say(text[0])

@client.command(pass_context=True)
async def scrape(ctx, url, tag, class_=None):
    url = url
    tag = tag
    c = class_

    r = requests.get(url)
    content = r.text

    urls = []
    text = []

    soup = BeautifulSoup(content, 'html.parser')
    if c:
        for p in soup.find_all(tag, class_=c):
            text.append(p.text)
        await client.say(text[random.randint(0, len(text) - 1)])
    if tag == 'image':
        for img in soup.find_all('img'):
            urls.append(img['src'])
        await client.say(urls[random.randint(0, len(urls) - 1)])

@client.command(pass_context=True)
async def wfa(ctx, *args):
    id = os.environ.get('WFA_ID')
    q = ' '.join(str(i) for i in args)
    if '+' in q:
        q = q.replace('+', 'plus')
    r = requests.get('http://api.wolframalpha.com/v2/query?appid=%s&input=%s&format=plaintext&output=json' % (id, q))
    data = r.json()
    await client.say(data['queryresult']['pods'][1]['subpods'][0]['plaintext'])

@client.command(pass_context=True)
async def bait(ctx, member: discord.Member):
    jebaits = []

    r2 = requests.get('https://myanimelist.net/news')
    content2 = r2.text
    r3 = requests.get('https://www.crunchyroll.com/news')
    content3 = r3.text

    text = []

    soup2 = BeautifulSoup(content2, 'html.parser')
    soup3 = BeautifulSoup(content3, 'html.parser')

    for n in soup2.find_all('div', class_='text'):
        text.append(n.text)
    for c in soup3.find_all('h2'):
        text.append(c.get_text())

    jebaits.append('BRAND SPANKIN NEW ANIME STRAIGHT OFF THE JAPANESE PRINTERS ELECTRONICALLY DIGITIZED INTO CRISP HIGH DEFINITION PIXEL JAPANESE GOODNESS!!!')
    jebaits.extend(text)

    await client.say(f'{member.mention}{jebaits[random.randint(0, len(jebaits) - 1)]}')


@client.command()
async def roll(numRolls, sides):
    rolls = []
    for i in range(int(numRolls)):
        r = random.randint(1, int(sides))
        await client.say(str(r) + f'/{sides}')
        rolls.append(r)
        total = 0
    for num in rolls:
        total += num
    await client.say(f'You rolled {total}')


@client.command(pass_context=True)
async def text(ctx, number, *args):
    if number == 'travis':
        number = os.environ.get('num1')
    if number == 'lewis':
        number = os.environ.get('num2')
    if number == 'doc':
        number = os.environ.get('num3')
    twilio = Client(account_sid, auth_token)
    twilio.messages.create(
        to=number,
        from_='+12564948478',
        body=' '.join(str(i) for i in args)
    )

# @client.command(pass_context=True)
# async def ffz(ctx, q):
#     #starttime = time.time()
#     if(q == 'monkaS'):
#         embed = discord.Embed(
#         title = 'monkaS',
#         colour = discord.Colour.green())
#         embed.set_image(url='https://cdn.frankerfacez.com/7ed3da04c09547097595ff979e629c36.png')
#         await client.say(embed=embed)
#     elif(q == None):
#         await client.say('Enter an arguement.')
#     elif(q == 'hypers'):
#         embed = discord.Embed(
#         title = 'hypers',
#         colour = discord.Colour.green())
#         embed.set_image(url='https://cdn.frankerfacez.com/2eca1ebdd82e120d31ab3b59e6aea68b.png')
#         await client.say(embed=embed)
#     elif(q == 'pepehands'):
#         embed = discord.Embed(
#         title = 'pepehands',
#         colour = discord.Colour.green())
#         embed.set_image(url='https://cdn.frankerfacez.com/b97ed9ea44a548134578aecd47348784.png')
#         await client.say(embed=embed)
#     else:
#         url = 'https://api.frankerfacez.com/v1/emoticons?q=%s&sort=count-desc' % q
#         s = requests.Session()
#         r = s.get(url).json()
#         # r = requests.get(url).json()

#     embed = discord.Embed(
#         title = q,
#         colour = discord.Colour.green())

#     try:
#         try:
#             res = 'https:',(r['emoticons'][0]['urls']['4'])
#             embed.set_image(url=''.join(res))
#             await client.say(embed=embed)
#         except KeyError:
#             res = 'https:',(r['emoticons'][0]['urls']['2'])
#             embed.set_image(url=''.join(res))
#             await client.say(embed=embed)
#     except KeyError:
#         res = 'https:',(r['emoticons'][0]['urls']['1'])
#         embed.set_image(url=''.join(res))
#         await client.say(embed=embed)


@client.command(pass_context=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)


@client.command(pass_context=True)
async def gal(ctx, s=3):
    if s == 1:
        await client.say('https://zippy.gfycat.com/RaggedChillyHoopoe.mp4')
    if s == 2:
        await client.say('https://bestofcomicbooks.com/wp-content/uploads/2018/06/gal-gadot-legs.gif')
    if s == 3:
        await client.say('https://gfycat.com/arctichideoushoneyeater')
    if s == 4:
        await client.say('https://gfycat.com/SplendidNextAsiaticgreaterfreshwaterclam')
    if s == 5:
        await client.say('https://bestofcomicbooks.com/wp-content/uploads/2018/06/gal-gadot-on-bed.gif')
    if s == 6:
        await client.say('https://bestofcomicbooks.com/wp-content/uploads/2018/06/gal-gadot-cleavage.gif')
    if s == 7:
        await client.say('https://bestofcomicbooks.com/wp-content/uploads/2018/06/gal-gadot-fantastic.gif')

@client.command(pass_context=True)
async def gif(ctx, *args):
    q = '+'.join(str(i) for i in args)
    urls = []

    try:
        r = requests.get(f'https://api.gfycat.com/v1/me/gfycats/search?search_text={q}&count=250')
        data = r.json()

        k = 0
        length = len(data['gfycats']) - 1
        while k < length:
            urls.append(data['gfycats'][k]['mp4Url'])
            k += 1


        await client.say('Here is what i found for: %s' % q)
        await client.say(urls[random.randint(0, len(urls) - 1)])

    except Exception as e:
        await client.say(e)

client.run(os.environ.get('BOT_TOKEN'))
