import requests
import json
import re
import csv
import os

from PIL import Image
from PIL import ImageSequence
from PIL import GifImagePlugin

import ffmpeg

GAME_STAT_PAGES = {
    'bfv': 'https://api.tracker.gg/api/v1/bfv/standard/profile/origin/{}',
    'apex': 'https://api.dreamteam.gg/games/apex/pc/players/{}/statistics',
    'r6s': 'https://r6stats.com/api/player-search/{}/pc',
    }

GAME_STAT_PAGE_FORMAT = {
    'bfv': '''Stats for origin alias: {}
              Score = {}
              Score/min: {}
              K/D: {}
              Kills: {}
              Deaths: {}
              Accuracy: {}
              Headshots: {}
              Longest headshot: {}
              playtime: {}''',
    'apex': '''Stats for origin alias: {}
               Rank: {} {}
               Rank points: {}/{}
               Kills as {}: {} kills''',
    'r6s': '''Stats for Ubisoft alias: {}
              Level: {}
              K/D: {}
              W/L: {}
              No. of games played: {}
              No. of suicides: {}''',

}

def get_game_stats(game, alias):
    if game in GAME_STAT_PAGES.keys():
        url = GAME_STAT_PAGES[game]
        response = requests.get(url.format(alias))
        print(response.json()[0].get('ubisoft_id'))
        if game == 'bfv':
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

                msg = GAME_STAT_PAGE_FORMAT[game].format(alias, 
                                                         score, 
                                                         spm,
                                                         kd,
                                                         kills, 
                                                         deaths, 
                                                         accr, 
                                                         heads, 
                                                         longhead, 
                                                         playtime)
                return msg
            except:
                print(response)
                msg = "Failed to find that player. Are you sure you spelled the alias correctly?"
                return msg

        elif game == 'apex':
            try:
                stats = response.json()
                rank = stats.get('player').get('rank').get('tier')
                div = stats.get('player').get('rank').get('division')
                legend = stats.get('statistics')[0].get('legend')
                kills = stats.get('statistics')[0].get('kills')
                level = stats.get('statistics')[1].get('level')
                rank_points = stats.get('statistics')[1].get('rank_points')
                next_rank_points = stats.get('player').get('rank').get('next_rank_points')

                msg = GAME_STAT_PAGE_FORMAT[game].format(alias, 
                                                         rank, 
                                                         div, 
                                                         rank_points, 
                                                         next_rank_points, 
                                                         legend, 
                                                         kills)
                return msg

            except:
                print(response)
                msg = "Failed to find that player. Are you sure you spelled the alias correctly?"
                return msg
        elif game == 'r6s':
            try:
                ubi_id = response.json()[0].get('ubisoft_id')
                ubi_response = requests.get('https://r6stats.com/api/stats/{}'.format(ubi_id))
                stats = ubi_response.json()
                level = stats.get('progression').get('level')
                kdratio = stats.get('stats')[0].get('general').get('kd')
                wlratio = stats.get('stats')[0].get('general').get('wl')
                suicide = stats.get('stats')[0].get('general').get('suicides')
                no_of_games = stats.get('stats')[0].get('general').get('games_played')
                
                msg = GAME_STAT_PAGE_FORMAT[game].format(alias,
                                                         level,
                                                         kdratio,
                                                         wlratio,
                                                         no_of_games,
                                                         suicide)

                return msg

            except:
                print(response)
                msg = "Failed to find that player. Are you sure you spelled the alias correctly?"
                return msg

    else:
        msg = 'I cannot find statistics for that game'
        return msg



def combine_mpeg(first_url, second_url):
    endfile = './tmp/combined.gif'
    first = './tmp/first.gif'
    second = './tmp/second.gif'

    with open(first, 'wb') as f, open (second, 'wb') as s:
        f.write(requests.get(first_url).content)
        s.write(requests.get(second_url).content)

    info = ffmpeg.probe(first)['streams'][0]
    f = ffmpeg.input(first)
    s = ffmpeg.input(second).filter('scale',
                                    width=info['width'], 
                                    height=info['height'], 
                                    force_original_aspect_ratio='decrease').filter('pad', 
                                            info['width'],
                                            info['height'],
                                            '(ow-iw)/2','(oh-ih)/2')
    ffmpeg.concat(f,s).output(endfile).overwrite_output().run()

    return endfile
