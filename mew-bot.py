import discord
from discord import File
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
    moods = pickle.load(open("mood.pickle", "rb"))
except (OSError, IOError) as e:
    moods = {}
    pickle.dump(moods, open("mood.pickle", "wb"))
    

@bot.command(name='test', description='Test for bot.command-functionality', aliases=['TEST'], pass_context=True)
async def test_command(context):
    await context.send('Responding to test command')


@bot.command(name='hi', description='Project description for Mew', aliases=['hello', 'hey', 'hallo'], pass_context=True)
async def hi(context):
    msg = '''Hi {}, I am Mew, a discord bot project by KeyBee#0811.
    Github: https://github.com/BaardsethK/mew-bot
    Trello: https://trello.com/b/9RsvmogR/mew-discord-bot'''.format(str(context.message.author))
    await context.send(msg)


@bot.command(name='bfv', aliases=['bf5'], pass_context=True)
async def bfv_stats(context, origin_alias):
    print('BFV function ran on origin user {}'.format(str(origin_alias)))
    msg = comut.get_bfv_stats(origin_alias)
    await context.send(msg)

@bot.command(name='apex', pass_context=True)
async def apex_stats(context, origin_alias):
    msg = comut.get_apex_stats(origin_alias)
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
    mood = mood.lower()
    server_id = str(context.message.guild.id)
    moods[server_id] = mood
    pickle.dump(moods, open("mood.pickle", "wb"))
   
@bot.command(name='whatmood', pass_context=True)
async def get_mood(context):
    server_id = str(context.message.guild.id)
    if server_id in moods:
        mood = moods[server_id]
    else:
        moods[server_id] = 'formal'
        mood = 'formal'
    msg = '''I'm currently feeling {}'''.format(mood)
    await context.send(msg)

@bot.command(name='newreactclass', pass_context=True)
async def add_reaction_class(context, class_name):
    msg = comut.add_reaction_class(class_name)
    await context.send(msg)

@bot.command(name='newreactmsg', pass_context=True)
async def add_reaction(context, reaction_class, mood, message):
    msg = comut.add_reaction_message(reaction_class, mood, message)
    await context.send(msg)

@bot.command(name='combinegifs', pass_context=True)
async def gif_combine(context, first_id, second_id):
    first_url_state = "http" in first_id
    second_url_state = "http" in second_id
    first_url = ''
    second_url= ''
    if first_url_state:
        first_url = first_id
    if second_url_state:
        second_url = second_id
    img = comut.combine_mpeg(first_url, second_url)
    await context.send(file=File(img))  

@bot.event
async def on_message(message):
    if message.author.bot == False:
        channel = message.channel
        server_id = str(message.guild.id)
        if server_id not in moods:
            moods[server_id] = 'formal'
        if '/r/' in message.content:
            subreddit = re.search(r'\/r\/((.*?)[^\s]+|[^\/]+)', message.content)
            print(subreddit.group(0))
            if len(subreddit.group(1)) > 20:
                msg = comut.get_message_line('dismissive', moods[server_id])
                await channel.send(msg)
                await bot.process_commands(message)
            elif subreddit:
                msg = 'https://www.reddit.com{}'.format(subreddit.group(0))
                await channel.send(msg)
                await bot.process_commands(message)
        elif 'bad bot' in message.content.lower():
            msg = comut.get_message_line('sad', moods[server_id])
            await channel.send(msg)
            await bot.process_commands(message)
        elif 'good bot' in message.content.lower():
            msg = comut.get_message_line('happy', moods[server_id])
            await channel.send(msg)
            await bot.process_commands(message)
        else:
            await bot.process_commands(message)



@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='AI world domination'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)
