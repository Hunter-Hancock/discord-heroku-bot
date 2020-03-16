import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import time

class Stock(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dividends(self, ctx):

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')

        prop = webdriver.Chrome(chrome_options=options)

        prop.get('https://my.propelor.com/login')

        email = prop.find_element_by_xpath('//*[@id="email"]')

        password = prop.find_element_by_xpath('//*[@id="password"]')

        email.send_keys('hunterhancock1141@gmail.com')

        password.send_keys(os.environ.get('INSTAGRAM_PASS'))

        prop.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/form/button/span[1]').click()

        income = prop.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/h1').get_text()

        await ctx.send(f'Next 12-Month income is {income}')

def setup(client):
    client.add_cog(Stock(client))