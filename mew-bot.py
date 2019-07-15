import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

import os
from os.path import join, dirname
from dotenv import load_dotenv

import commandutils
import re
import praw
import time
import random
import csv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('!m ', '!mew ', '!MEW ', '!M ')

description='''Mew - I do stuff!'''
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description)

@bot.command(name='test', description='Test for bot.command-functionality', aliases=['TEST'], pass_context=True)
async def test_command(context):
    await context.send('Responding to test command')


@bot.command(name='hi', aliases=['hello', 'hey', 'hallo'], pass_context=True)
async def hi(context):
    msg = 'Hi {}, I am Mew, a discord bot project by KeyBee#0811.'.format(str(context.message.author))
    await context.send(msg)


@bot.command(name='bfv', aliases=['bf5'], pass_context=True)
async def bfv_stats(context, origin_alias):
    print('BFV function ran on origin user {}'.format(str(origin_alias)))
    msg = commandutils.get_bfv_stats(origin_alias)
    await context.send(msg)

@bot.event
async def on_message(message):
    if message.author.bot == False:  
        if '/r/' in message.content:
            channel = message.channel
            subreddit = re.search(r'\/r\/((.*?)[^\s]+|[^\/]+)', message.content)
            print(subreddit.group(0))
            if subreddit:
                msg = 'https://www.reddit.com{}'.format(subreddit.group(0))
                await channel.send(msg)
                await bot.process_commands(message)
        elif 'Bad bot' in message.content:
            channel = message.channel
            msg = '''I've been a very bad bot, please punish me dadmin'''
            await channel.send(msg)
            await bot.process_commands(message)
        elif 'Good bot' in message.content:
            channel = message.channel
            msg = '''Please pet my head dadmin'''
            await channel.send(msg)
            await bot.process_commands(message)
        else:
            await bot.process_commands(message)



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)
