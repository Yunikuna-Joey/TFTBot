# imports 
from dotenv import load_dotenv
from riotwatcher import LolWatcher
import requests
import os 


# loads the variables to be used in this py file 
load_dotenv()
rga = os.getenv('API_KEY')

# Establishes connection to RGA via key (The key must be explicitly stated in main file)
watcher = LolWatcher(rga) 

# Gives initial region to start with 
region_value = 'NA1'
name = 'Yunikuna'

# name_data returns a dictionary so therefore variable is type dict 
name_data = watcher.summoner.by_name(region_value, name)
print(name_data)

# formatting string output for concatenating key-value
print('Your summoner level is: %s' % name_data['summonerLevel'])


# Testing champion stuff here 

# the url that will be accessed for champion rotation data
url = f'https://na1.api.riotgames.com/lol/platform/v3/champion-rotations'
headers = {"X-Riot-Token": rga}
response = requests.get(url, headers=headers)

# HTTP status codes 
    # 1xx informational 
    # 2xx success 
    # 3xx redirect
    # 4xx client error
    # 5xx server error  

# if there is successful connected denoted by status code 2xx
if response.status_code == 200: 
    print(response.json()['freeChampionIds'])

else: 
    print(f"Failed to fetch free champions. Status code: {response.status_code}")
    print("None")

# testing if we can get the names of the champions in the rotation 
def champ_info(champion_id):
    url = f'https://na1.api.riotgames.com/lol/champions/{champion_id}'
    headers = {'X-Riot-TOken': rga}

    try: 
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        champion_info = response.json()
        return champion_info
    
    except requests.exceptions.RequestException as e: 
        print('Error: ', e)
        return None
    
a = int(input("What is the champion number you are looking for? "))
champ_info(a)