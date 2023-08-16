# ********** THIS FILE WILL BE USED FOR DISPLAYING JSON DATA TO BE MANIPULATED **********
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

# ign and region of the said user
regionValue = 'NA1'
ign = 'Yunikuna'

lwatcher = LolWatcher(rga)
name_data = lwatcher.summoner.by_name(regionValue, ign)

print(name_data)

