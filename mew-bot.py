import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

import os
from os.path import join, dirname
from dotenv import load_dotenv

import commandutils as comut
import re
import praw
import time
import random
import csv
import pickle

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('!m ', '!mew ', '!Mew ', '!MEW ', '!M ')

description='''Mew - I do stuff!'''
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description)


try:
    mood = pickle.load(open("mood.pickle", "rb"))
except (OSError, IOError) as e:
    mood = {"":"formal"}
    pickle.dump(mood, open("mood.pickle", "wb"))
    

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
    msg = comut.get_bfv_stats(origin_alias)
    await context.send(msg)

@bot.command(name='uwuize', aliases=['uwu'], pass_context=True)
async def uwuize(context, *, message):
    msg = message.lower()
    msg = msg.replace('pos', 'paws')
    msg = msg.replace('r', 'w')
    msg = msg.replace('l', 'w')
    msg = msg.replace('th', 'd')
    await context.send(msg)
    
@bot.command(name='moodify', aliases=['mood'], pass_context=True)
async def save_mood(context, mood):
    server_id = context.message.server.id
    mood[server_id] = mood
    pickle.dump(mood, open("mood.pickle", "wb"))
    
@bot.event
async def on_message(message):
    if message.author.bot == False:
        channel = message.channel
        server_id = message.guild.id
        if '/r/' in message.content:
            subreddit = re.search(r'\/r\/((.*?)[^\s]+|[^\/]+)', message.content)
            print(subreddit.group(0))
            if len(subreddit.group(1)) > 20:
                msg = comut.get_message_line('dismissive', mood[server_id])
                await channel.send(msg)
                await bot.process_commands(message)
            elif subreddit:
                msg = 'https://www.reddit.com{}'.format(subreddit.group(0))
                await channel.send(msg)
                await bot.process_commands(message)
        elif 'bad bot' in message.content.lower():
            msg = comut.get_message_line('sad', mood[server_id])
            await channel.send(msg)
            await bot.process_commands(message)
        elif 'good bot' in message.content.lower():
            msg = comut.get_message_line('happy', mood[server_id])
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
