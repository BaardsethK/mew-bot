import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import bot

import os
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

import re
import pickle
import random

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('!mew ')

JAR = ('./discord.pkl')

description = '''Mew - Python-based discord bot!'''
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description)

@bot.command(name='hi', description='Project description for Mew', aliases=['hello', 'hey', 'hallo'], pass_context=True)
async def hi(context):
    msg = '''Hi {}, I am Mew, a discord bot project by KeyBee#0811.
    Github: https://github.com/BaardsethK/mew-bot
    Trello: https://trello.com/b/9RsvmogR/mew-discord-bot'''.format(str(context.message.author))
    await context.send(msg)

@bot.command(name='uwuize', pass_context=True)
async def uwuize(context, *, message):
    msg = message.lower()
    msg = msg.replace('pos', 'paws')
    msg = msg.replace('r', 'w')
    msg = msg.replace('l', 'w')
    msg = msg.replace('th', 'd')
    await context.send(msg)

@bot.command(name='score', pass_context=True)
async def score(context):
    if os.path.getsize(JAR) > 0:
        pickle_data = pickle.load(open(JAR, "rb"))
        if hash(context.message.author) in pickle_data:
            score = pickle_data[hash(context.message.author)]
            msg = f"Your content score is {score}"
            await context.send(msg)
    else:
        msg = "You have no content score. Send attachments to score better!"
        await context.send(msg)

@bot.command(name='roll',
    description='Runs one of the roll-commands available',
    pass_context=True)
async def roll(context, limit=100):
    roll = random.randint(0,1)
    if roll == 0:
        await rollMsg(context, limit)
    else:
        await rollImg(context, limit)

@bot.command(name='rollmsg',
    description='Roll random message from message history. Limit is 100 msg history unless specified',
    pass_context=True)
async def rollMsg(context, msg_limit = 100):
    messages = await context.channel.history(limit=msg_limit).flatten()
    msg_txt = []
    for historic_msg in messages:
        if len(historic_msg.content) > 0 and '!mew' not in historic_msg.content:
            msg_txt.append(f"> {historic_msg.author}: {historic_msg.content}")
    max_roll = len(msg_txt)
    if max_roll == 0:
        await context.send("No messages available!")
    elif max_roll > 0:
        roll = random.randint(0, max_roll - 1)
        msg = msg_txt[roll]
        await context.send(msg)

@bot.command(name='rollimg',
    description='Roll random image from message history. Limit is 100 msg history unless specified',
    pass_context=True)
async def rollImg(context, msg_limit = 100):
    messages = await context.channel.history(limit=msg_limit).flatten()
    msg_attachments = []
    for historic_msg in messages:
        if len(historic_msg.attachments) > 0:
            msg_attachments.append(historic_msg.attachments[0])
    max_roll = len(msg_attachments)
    if max_roll == 0:
        await context.send("No images/attachments available!")
    elif max_roll > 0:
        roll = random.randint(0, max_roll-1)
        file_to_send = await msg_attachments[roll].to_file()
        await context.send(file=file_to_send)

async def addscore(author):
    if os.path.getsize(JAR) > 0:
        pickle_data = pickle.load(open(JAR, "rb"))
    else:
        print("No pickle-file, EOFError")
        print("Creating pickle data")
        pickle_data = {}
    if author in pickle_data:
        score = pickle_data[author]
        pickle_data[author] = score + 1
    elif author not in pickle_data:
        pickle_data[author] = 1

    outfile = open(JAR, 'wb')

    pickle.dump(pickle_data, outfile)
    outfile.close() 
    


@bot.event
async def on_message(message):
    if message.author.bot == False:
        channel = message.channel
        server_id = str(message.guild.id)
        if '/r/' in message.content:
            subreddit = re.findall(r'\/r\/([a-zA-Z0-9]+[^\W]|[^\D])', message.content)
            if subreddit:
                for sub in subreddit:
                    msg = f'https://www.reddit.com/r/{sub}'
                    await channel.send(msg)
        if len(message.attachments) > 0:
            author = hash(message.author)
            await addscore(author)
        await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=''))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)