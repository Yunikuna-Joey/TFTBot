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
        # if the data is a DICTIONARY in a LIST --> use the first index and call upon as the dictionary k/v
        wins = entry['wins']
        loss = entry['losses']
        print( (wins/loss) * 100)
        print(data)

    else: 
        print(f'Error: {response.status_code}')    

# display player rank 
def displayRank(id): 
    # tft test
    base_url = f'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{id}'
    headers = {"X-Riot-Token" : rga}


    response = requests.get(base_url, headers=headers)

    if response.status_code == 200: 
        # formats the data to be in JSON format to be extracted 
        data = response.json() 

        display = data[0]
        player_rank = display['tier']
        player_tier = display['rank'] 

        print('Your current rank is ' + player_rank + ' ' + player_tier)

def status(): 
    # API call 
    url = f'https://na1.api.riotgames.com/tft/status/v1/platform-data?api_key=' + rga
    headers = {'X-Riot-Token': rga} 

    response = requests.get(url, headers=headers)
    
    # successful http code 
    if response.status_code == 200: 
        data = response.json()
        print('Ran tft status command')

        # should have the output 'North America' (true)
        entry = data['name']

        hehe = data['maintenances'][0]


        status  = hehe['maintenance_status']

        # a = hehe['titles'][0]

        # b = a['content']


        # print(data)
        # print(entry)

        # Has the output: in_progress 
        print(status)


        # Has the output: Split End Transfers Disabled 
        # print(b)
    
    else: 
        print(f'Error code: {response.status_code}')


# -------------------------------------------------------------------------
# main class if you will 
# tftProfile(id)
# tftWinRate(id)
# displayRank(id)
status()






