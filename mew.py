import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import CommandNotFound

import os
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

import re
import pickle
import random
import databasehandler

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('!mew ')

CURRENCY_DATABASE = ('./sqlite/db/currencybase.db')

description = '''Mew - Python-based discord bot!'''
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description, intents=intents)


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

@bot.command(name='initdb', description='Init DB file/tables if not exists', pass_context=True)
async def init_db(context):
    databasehandler.init_databases(CURRENCY_DATABASE)
    await context.send('Initiated')

@bot.command(name='score', pass_context=True)
async def score(context):
    score =  databasehandler.check_user(CURRENCY_DATABASE, context.message.author.id)
    msg = f"Your content score is {score[2]}"
    await context.send(msg)

@bot.command(name='hiscore', description='Check current server Hi-score',pass_context=True)
async def hiscore(context):
    users = context.guild.members
    scoreboard = {}
    msg = "Scores:\n"
    for user in users:
        if user.nick:
            name = user.nick
        else:
            name = user
        scoreboard[name] = await checkUserScore(user)
    scoreboard = dict(sorted(scoreboard.items(), key=lambda item: item[1], reverse=True))
    for user,score in scoreboard.items():
        msg += f"\t{user}: {score}\n"
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

@bot.command(name='rolluser',
    description='Roll a random user to go with your message',
    pass_context=True)
async def rollUser(context, *, arg = ""):
    members = context.channel.members
    member = members[random.randint(0, len(members)-1)]
    if len(arg) > 0:
        msg = f"{member.display_name} {arg}"
    else:
        msg = f"{member.display_name}"
    await context.send(msg)

@bot.event
async def on_message(message):
    if message.author.bot == False:
        channel = message.channel
        server_id = str(message.guild.id)
        if '/r/' in message.content:
            subreddit = re.findall(r'\/r\/[a-zA-Z0-9_.-]{3,20}', message.content)
            if subreddit:
                for sub in subreddit:
                    msg = f'https://www.reddit.com{sub}'
                    await channel.send(msg)
        if len(message.attachments) > 0:
            author = message.author.id
            await score_user(100, author)
        await bot.process_commands(message)

async def score_user(score, user_id):
    user_data = databasehandler.check_user(CURRENCY_DATABASE, (user_id))
    if user_data is None:
        databasehandler.add_user(CURRENCY_DATABASE, (user_id, 0,0))
    elif user_data is not None:
        databasehandler.increase_user_score(CURRENCY_DATABASE, (score, user_id))

@bot.event
async def on_command_error(context, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=''))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)