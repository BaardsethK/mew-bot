import requests
import json
import re
import csv



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
            
            
def get_message_line(msg_type, mood_type):
    msg = ''
    with open('lines.json') as msg_file:
        data = json.load(msg_file) 
        data = data[msg_type]
        msg_data = next((item for item in data if item["mood"] == mood_type))
        msg = msg_data["msg"]
        return msg
