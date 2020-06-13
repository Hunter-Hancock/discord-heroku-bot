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
from webdriver_manager.chrome import ChromeDriverManager

import json
import re

client = commands.Bot(command_prefix='!')

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

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Extension loaded!')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('Extension unloaded!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
    if filename[:-3] == 'spoilers':
            client.unload_extension(f'cogs.spoilers')

@client.command()
async def instagram(ctx, account):
    # bot = webdriver.Chrome()
    # bot.get('https://instagram.com/')
    # time.sleep(2)
    # loginbtn = bot.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a').click()
    # time.sleep(2)
    # time.sleep(1)
    # username = bot.find_element_by_name('username')
    # user = os.environ.get('INSTAGRAM_USER')
    # passw = os.environ.get('INSTAGRAM_PASS')
    # username.send_keys(user)
    # password = bot.find_element_by_name('password')
    # password.send_keys(passw)
    # password.send_keys(Keys.RETURN)
    # time.sleep(2)
    # bot.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
    bot = webdriver.Chrome(ChromeDriverManager().install())
    # bot = webdriver.Chrome()
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
async def imgur(ctx, *args):

    search = '+'.join(str(i) for i in args)
    res = [item for item in imgclient.gallery_search(
        search, sort='top', window='all')]

    if (len(res) == 0):
        await ctx.send('Sorry no results for: %s' % search)
    else:
        await ctx.send('Here is what i found for: %s on imgur' % search)
        await ctx.send(res[random.randint(0, len(res))].link)


@client.command()
async def translate(ctx, *args):
    imsg = ''.join(str(i) for i in args)
    # tmsg = translator.translate(imsg, dest=lang)
    tmsg = translator.translate(imsg, dest='en')
    # await ctx.send(f'Translating from {tmsg.src} to {tmsg.dest}')
    await ctx.send(tmsg.text)

@client.command()
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

    await ctx.send(f'Here is the latest patch notes for {q}.') 
    # await ctx.send(embed=embed)
    await ctx.send(posts[0].url)

    if len(posts) == 0:
        await ctx.send("Didn't find patch")

@client.command()
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
        await ctx.send(text[random.randint(0, len(text) - 1)])
    if tag == 'image':
        for img in soup.find_all('img'):
            urls.append(img['src'])
        await ctx.send(urls[random.randint(0, len(urls) - 1)])

@client.command()
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

    await ctx.send(urls[random.randint(0, len(urls) - 1)])
    browser.quit()

@client.command()
async def filler(ctx, *args):
    ep = []
    search = '-'.join(str(i) for i in args)

    r = requests.get(f'https://www.animefillerlist.com/shows/{search}')
    content = r.text

    try:
        soup = BeautifulSoup(content, 'html.parser')
        body = soup.body.find(text=re.compile('[0-9][0-9][%]'))
        filler_percentage = re.findall('[0-9][0-9][%]', str(body.encode('utf-8')))
        # filler_percentage = ''.join(re.split('[0-9][0-9][%]', str(body.encode('utf-8'))))
        episodes = soup.findAll('span', class_='Episodes')
        episode = episodes[2]
        for child in episode.children:
            ep.append(child.string.strip(' ,'))

        ep = list(filter(None, ep))
        ep_string = ', '.join(ep)
        await ctx.send(f"Episodes {ep_string} are filler. {search.capitalize()}'s filler percentage is {filler_percentage[0]}")
    except Exception as e:
        print(e)
        await ctx.send(f'Could not find {search}.')

@client.command()
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

    await ctx.send(f'{member.mention}{jebaits[random.randint(0, len(jebaits) - 1)]}')

@client.command()
async def roll(ctx,numRolls, sides):
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

@client.command()
async def clear(ctx, amount):
    channel = ctx.channel
    await channel.purge(limit=int(amount))

@client.command()
async def gal(ctx, s=3):
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

client.run(os.environ.get('BOT_TOKEN'))