import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

import os
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

import commandutils
import re
import time
import random
import csv
import pickle

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('!m ', '!mew ', '!Mew ', '!MEW ', '!M')

description='''Mew - Python-based discord bot!'''
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description)

@bot.commad(name='hi', description='Project description for Mew', aliases=['hello', 'hey', 'hallo'], pass_context=True)
async def hi(context):
    msg = '''Hi {}, I am Mew, a discord bot project by KeyBee#0811.
    Github: https://github.com/BaardsethK/mew-bot
    Trello: https://trello.com/b/9RsvmogR/mew-discord-bot'''.format(str(context.message.author))
    await context.send(msg)

@bot.command(name='gamestat', pass_context=True)
async def gamestat(context, game, alias):
    msg = commandutils.get_game_stats(game, alias)
    await context.send(msg)

@bot.command(name='uwuize', aliases=['uwu'], pass_context=True)
async def uwuize(context, *, message):
    msg = message.lower()
    msg = msg.replace('pos', 'paws')
    msg = msg.replace('r', 'w')
    msg = msg.replace('l', 'w')
    msg = msg.replace('th', 'd')
    await context.send(msg)

@bot.event
async def on_message(message):
    if message.author.bot == False:
        channel = message.channel
        server_id = str(message.guild.id)
        if '/r/' in message.content:
            subreddit = re.search(r'\/r\/((.*?)[^\s-.-,]+|[^\/]+)', message.content)
            print(subreddit.group(0))
            if len(subreddit.group(1)) > 20:
                msg = comut.get_message_line('dismissive', moods[server_id])
                await channel.send(msg)
                await bot.process_commands(message)
            elif subreddit:
                msg = 'https://www.reddit.com{}'.format(subreddit.group(0))
                await channel.send(msg)
                await bot.process_commands(message)
        else:
            await bot.process_commands(message)

@bot.event
async def on_reay():
    await bot.change_presence(activity=discord.Game(name=''))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)