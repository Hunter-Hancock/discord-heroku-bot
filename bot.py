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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json

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
    game = discord.Game('!gif !imgur !reddit !nsfw')
    await client.change_presence(status=discord.Status.online, activity=game)
    # await client.change_presence(game=discord.Game(name='!gif !imgur !reddit !nsfw'))

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['name'] = user.display_name
        users[user.id]['chips'] = 1000

@client.command()
async def blackjack(bet):

    with open('blackjack.json', 'r') as f:
        users = json.load(f)

    await update_data(users, ctx.message.author)

    if int(bet) > users[ctx.message.author.id]['chips']:
        await ctx.send(f"Not enough chips. You only have: {users[ctx.message.author.id]['chips']}")
        users[ctx.message.author.id]['chips'] += int(bet)
    
    users[ctx.message.author.id]['chips'] -= int(bet)

    player_card1 = random.randint(2, 10)
    player_card2 = random.randint(2, 10)
    player_total = player_card1 + player_card2

    dealer_card1 = random.randint(2, 10)
    dealer_card2 = random.randint(2, 10)
    dealer_total = dealer_card1 + dealer_card2

    player_hand = [player_card1, player_card2]
    dealer_hand = [dealer_card1, dealer_card2]

    await ctx.send(f'Dealer has: {dealer_card1} you have: {player_hand}')
    await ctx.send('Do you want to hit or stand?')
    # response = await client.wait_for_message('message')
    response = await client.wait_for('message', check='hit')

    if response.content == 'hit':
        await ctx.send('You hit!')
        new_card = random.randint(2, 10)
        player_hand.append(new_card)
        await ctx.send(f'You now have {player_hand}')

    if response == 'stand':
        pass

    with open('blackjack.json', 'w') as f:
        json.dump(users, f)

@client.command()
async def chips(ctx):
    with open('blackjack.json', 'r') as f:
        users = json.load(f)
    await ctx.send(users[ctx.message.author.id]['chips'] + 'chips')

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
#     await ctx.send(messages)

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

@client.command()
async def instagram(account):
    bot.get('https://instagram.com/')
    time.sleep(2)
    loginbtn = bot.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a').click()
    time.sleep(2)
    time.sleep(1)
    username = bot.find_element_by_name('username')
    user = os.environ.get('INSTAGRAM_USER')
    passw = os.environ.get('INSTAGRAM_PASS')
    username.send_keys(user)
    password = bot.find_element_by_name('password')
    password.send_keys(passw)
    password.send_keys(Keys.RETURN)
    time.sleep(2)
    bot.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
    bot = webdriver.Chrome()
    bot.get(f'https://instagram.com/{account}')
    time.sleep(1)
    soup = BeautifulSoup(bot.page_source, 'lxml')
    content = soup.find_all('div', class_='KL4Bh')
    count = 0
    if count == 0:
        for post in content:
            image = post.find('img')
            await ctx.send(image['src'])
        videos = soup.find_all('div', class_='_5wCQW')
        for v in videos:
            video = v.find('video')
            await ctx.send(video['src'])
            count += 1
    bot.quit()

@client.command()
async def scrape2(website, class_name):
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

    await ctx.send(urls[random.randint(0, len(urls) - 1)])
    browser.quit()

@client.command()
async def nsfw(ctx):
    browser = webdriver.Chrome()
    browser.get('https://scrolller.com/')

    nsfw = browser.find_element_by_css_selector('body > div.center-bar > div > div > div:nth-child(2) > a:nth-child(3) > div > div').click()
    women = browser.find_element_by_css_selector('#intro-settings > div > div > div > div:nth-child(3) > div:nth-child(2) > div').click()

    time.sleep(4)

    soup = BeautifulSoup(browser.page_source, 'lxml')
    image = soup.find_all('div', class_='fill-size')

    urls = []

    for img in image:
        if img.find('img') is not None and img.find('video') == None:
            links = img.find('img')
            urls.append(links['src'])
        else:
            links = img.find('video')
            urls.append(links.source['src'])

    await ctx.send(urls[random.randint(0, len(urls) - 1)])
    browser.quit()

@client.command()
async def snap(ctx):
    channel = ctx.message.channel
    await ctx.send('SNAP!')
    time.sleep(.5)
    await ctx.send('https://tenor.com/view/iam-iron-man-iron-man-avengers-endgame-avengers-endgame-gif-14042823')
    async for message in client.logs_from(channel, limit=6):
        time.sleep(7)
        await client.delete_message(message)

@client.command()
async def imgur(*args):

    search = '+'.join(str(i) for i in args)
    res = [item for item in imgclient.gallery_search(
        search, sort='top', window='all')]

    if (len(res) == 0):
        await ctx.send('Sorry no results for: %s' % search)
    else:
        await ctx.send('Here is what i found for: %s on imgur' % search)
        await ctx.send(res[random.randint(0, len(res))].link)


@client.command()
async def translate(*args):
    imsg = ''.join(str(i) for i in args)
    # tmsg = translator.translate(imsg, dest=lang)
    tmsg = translator.translate(imsg, dest='en')
    # await ctx.send(f'Translating from {tmsg.src} to {tmsg.dest}')
    await ctx.send(tmsg.text)

@client.command()
async def patch(q):
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

    await ctx.send('Here is the latest patch notes for %s.' % q)
    # await ctx.send(embed=embed)
    await ctx.send(posts[0].url)

    if len(posts) == 0:
        await ctx.send("Didn't find patch")

@client.command()
async def reddit(*args):
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
    await ctx.send(embed=embed)
    await ctx.send('https://www.reddit.com/comments/%s' % wadu.id)

@client.command()
async def avatar(ctx):
    user = ctx.message.author
    if user.avatar == None:
        await ctx.send('https://cdn.discordapp.com/embed/avatars/0.png')
    else:
        await ctx.send(user.avatar_url)

@client.command()
async def tomatoes(*args):
    text = []
    q = '_'.join(str(i) for i in args)
    r = requests.get(f'https://www.rottentomatoes.com/m/{q}')
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
    for i in soup.find_all('span', class_='mop-ratings-wrap__percentage'):
        text.append(i.text)
    await ctx.send(text[0])

@client.command()
async def scrape(url, tag, class_=None):
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
        await ctx.send(text[random.randint(0, len(text) - 1)])
    if tag == 'image':
        for img in soup.find_all('img'):
            urls.append(img['src'])
        await ctx.send(urls[random.randint(0, len(urls) - 1)])

@client.command()
async def wfa(*args):
    id = os.environ.get('WFA_ID')
    q = ' '.join(str(i) for i in args)
    if '+' in q:
        q = q.replace('+', 'plus')
    r = requests.get('http://api.wolframalpha.com/v2/query?appid=%s&input=%s&format=plaintext&output=json' % (id, q))
    data = r.json()
    await ctx.send(data['queryresult']['pods'][1]['subpods'][0]['plaintext'])

@client.command()
async def bait(member: discord.Member):
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

    await ctx.send(f'{member.mention}{jebaits[random.randint(0, len(jebaits) - 1)]}')

@client.command()
async def roll(numRolls, sides):
    rolls = []
    for i in range(int(numRolls)):
        r = random.randint(1, int(sides))
        await ctx.send(str(r) + f'/{sides}')
        rolls.append(r)
        total = 0
    for num in rolls:
        total += num
    await ctx.send(f'You rolled {total}')

@client.command()
async def text(number, *args):
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

# @client.command()
# async def ffz(q):
#     #starttime = time.time()
#     if(q == 'monkaS'):
#         embed = discord.Embed(
#         title = 'monkaS',
#         colour = discord.Colour.green())
#         embed.set_image(url='https://cdn.frankerfacez.com/7ed3da04c09547097595ff979e629c36.png')
#         await ctx.send(embed=embed)
#     elif(q == None):
#         await ctx.send('Enter an arguement.')
#     elif(q == 'hypers'):
#         embed = discord.Embed(
#         title = 'hypers',
#         colour = discord.Colour.green())
#         embed.set_image(url='https://cdn.frankerfacez.com/2eca1ebdd82e120d31ab3b59e6aea68b.png')
#         await ctx.send(embed=embed)
#     elif(q == 'pepehands'):
#         embed = discord.Embed(
#         title = 'pepehands',
#         colour = discord.Colour.green())
#         embed.set_image(url='https://cdn.frankerfacez.com/b97ed9ea44a548134578aecd47348784.png')
#         await ctx.send(embed=embed)
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
#             await ctx.send(embed=embed)
#         except KeyError:
#             res = 'https:',(r['emoticons'][0]['urls']['2'])
#             embed.set_image(url=''.join(res))
#             await ctx.send(embed=embed)
#     except KeyError:
#         res = 'https:',(r['emoticons'][0]['urls']['1'])
#         embed.set_image(url=''.join(res))
#         await ctx.send(embed=embed)


@client.command()
async def clear(amount):
    channel = ctx.channel
    await channel.purge(limit=int(amount))

    # channel = ctx.channel
    # messages = []
    # async for message in channel.history(limit=int(amount)):
    #     messages.append(message)
    # await client.delete_messages(messages)


@client.command()
async def gal(s=3):
    if s == 1:
        await ctx.send('https://zippy.gfycat.com/RaggedChillyHoopoe.mp4')
    if s == 2:
        await ctx.send('https://bestofcomicbooks.com/wp-content/uploads/2018/06/gal-gadot-legs.gif')
    if s == 3:
        await ctx.send('https://gfycat.com/arctichideoushoneyeater')
    if s == 4:
        await ctx.send('https://gfycat.com/SplendidNextAsiaticgreaterfreshwaterclam')
    if s == 5:
        await ctx.send('https://bestofcomicbooks.com/wp-content/uploads/2018/06/gal-gadot-on-bed.gif')
    if s == 6:
        await ctx.send('https://bestofcomicbooks.com/wp-content/uploads/2018/06/gal-gadot-cleavage.gif')
    if s == 7:
        await ctx.send('https://bestofcomicbooks.com/wp-content/uploads/2018/06/gal-gadot-fantastic.gif')

@client.command()
async def gif(*args):
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

        await ctx.send('Here is what i found for: %s' % q)
        await ctx.send(urls[random.randint(0, len(urls) - 1)])

    except Exception as e:
        await ctx.send(e)

client.run(os.environ.get('BOT_TOKEN'))
