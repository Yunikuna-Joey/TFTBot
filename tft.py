# imports 
from dotenv import load_dotenv
from riotwatcher import LolWatcher
import requests
import os 
import json

# HTTP status codes 
    # 1xx informational 
    # 2xx success 
    # 3xx redirect
    # 4xx client error
    # 5xx server error  

# loads the variables to be used in this py file 
load_dotenv()
rga = os.getenv('API_KEY')

# create a watcher so that information can be passed 
watcher = LolWatcher(rga)

# ign and region of the said user
regionValue = 'NA1'
ign = 'Yunikuna'

# profile information about user
name_data = watcher.summoner.by_name(regionValue, ign)
# lists out the information in a json dictionary to be extracted 
# print(name_data)
id = name_data['id']

def tftProfile(id): 
    # tft test
    base_url = f'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{id}'
    headers = {"X-Riot-Token" : rga}


    response = requests.get(base_url, headers=headers)

    if response.status_code == 200: 
        data = response.json() 
        print(data)

    else: 
        print(f'Error: {response.status_code}')

def tftWinRate(id): 
    # tft test
    base_url = f'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{id}'
    headers = {"X-Riot-Token" : rga}


    response = requests.get(base_url, headers=headers)

    if response.status_code == 200: 
        data = response.json() 
        # print('Win Rate: ' + data['wins'] / data['losses'])
        # data is a list here
        entry = data[0]
        wins = entry['wins']
        loss = entry['losses']
        print('Win Rate: ' + wins/loss)

    else: 
        print(f'Error: {response.status_code}')    

# -------------------------------------------------------------------------
# main class if you will 
# tftProfile(id)
tftWinRate(id)





