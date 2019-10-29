import requests
import json
import re
import csv
import os
from PIL import Image, ImageSequence, GifImagePlugin
import ffmpeg



def get_bfv_stats(origin_alias):
        response = requests.get('https://api.tracker.gg/api/v1/bfv/standard/profile/origin/{}'.format(origin_alias))
        try:
            stats = response.json().get('data').get('stats')
            spm = round(float(stats[0].get('value')), 2)
            kd = round(float(stats[1].get('value')), 2)
            kills = stats[2].get('value')
            deaths = stats[3].get('value')
            accr = round(float(stats[10].get('value')), 2)
            heads = stats[15].get('value')
            longhead = stats[17].get('value')
            playtime = stats[37].get('displayValue')
            score = stats[38].get('value')
            msg = '''Stats for origin alias: {}
            Score = {}
            Score/min: {}
            K/D: {}
            Kills: {}
            Deaths: {}
            Accuracy: {}
            Headshots: {}
            Longest headshot: {}
            playtime: {}'''.format(origin_alias, score, spm, kd, kills, deaths, accr, heads, longhead, playtime)
            return msg
        except:                                                                                                                                                                                                
            msg = "Failed to find that player. Are you sure you spelled it correctly?"
            return msg
           
def get_apex_stats(origin_alias):
    response = requests.get('https://api.dreamteam.gg/games/apex/pc/players/{}/statistics'.format(origin_alias))
    try:
        stats = response.json()
        rank = stats.get('player').get('rank').get('tier')
        div = stats.get('player').get('rank').get('division')
        legend = stats.get('statistics')[0].get('legend')
        kills = stats.get('statistics')[0].get('kills')
        level = stats.get('statistics')[1].get('level')
        rank_points = stats.get('statistics')[1].get('rank_points')
        next_rank_points = stats.get('player').get('rank').get('next_rank_points')

        msg = '''Stats for origin alias: {}
        Rank: {} {}
        Rank points: {}/{}
        Kills as {}: {} kills
        '''.format(origin_alias, rank, div, rank_points, next_rank_points, legend, kills)
        return msg
    except:
        print(response)
        msg = "Failed to find that player. Are you sure you spelled it correctly?"
        return msg
            
def get_message_line(msg_type, mood_type):
    msg = ''
    with open('lines.json') as msg_file:
        data = json.load(msg_file) 
        data = data[msg_type]
        msg_data = next((item for item in data if item["mood"] == mood_type))
        msg = msg_data["msg"]
        return msg

def add_reaction_class(reaction_class):
    reaction_class = reaction_class.lower()
    with open('lines.json') as msg_file:
        data = json.load(msg_file)
        class_exists = reaction_class in data
    if not class_exists:
        with open('lines.json', 'w') as msg_file:
            data[reaction_class] = ''
            json.dump(data, msg_file)
        return 'Message class "{}" created'.format(reaction_class)
    else:
        return 'Message class "{}" already exists'.format(reaction_class)

def add_reaction_message(reaction_class, reaction_mood, message):
    reaction_class = reaction_class.lower()
    reaction_mood = reaction_mood.lower()
    with open('lines.json') as msg_file:
        data = json.load(msg_file)
        class_exists = reaction_class in data
        try:
            msg_class = data[reaction_class]
            for item in msg_class:
                if (item['mood'] == reaction_mood):
                    mood_exists = True
        except KeyError:
            mood_exists = False
            pass
    if class_exists and not mood_exists:
        with open('lines.json','w') as msg_file:
            data[reaction_class].append({"mood": reaction_mood, "msg" :message})
            json.dump(data,msg_file)
            print('Added message {0}:{1} to class {2}'.format(reaction_mood, message, reaction_class))
        return 'Added message reaction to file'
    elif class_exists and mood_exists:
        return 'This class mood and message already exists. You should make a pull request to change it, or ask the developer to get off his ass and do it himself'
    elif not class_exists and not mood_exists:
        return 'Class does not exist.'

def combine_mpeg(first_url, second_url):
    endfile = './tmp/combined.gif'
    first = './tmp/first.gif'
    second = './tmp/second.gif'

    with open(first, 'wb') as f, open (second, 'wb') as s:
        f.write(requests.get(first_url).content)
        s.write(requests.get(second_url).content)

    info = ffmpeg.probe(first)['streams'][0]
    f = ffmpeg.input(first)
    s = ffmpeg.input(second).filter('scale',width=info['width'], height=info['height'], force_original_aspect_ratio='decrease').filter('pad', info['width'], info['height'], '(ow-iw)/2','(oh-ih)/2')
    ffmpeg.concat(f,s).output(endfile).overwrite_output().run()

    return endfile
