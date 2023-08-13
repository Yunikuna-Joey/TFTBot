# imports for discord bot
import os
import random
import discord
import requests 

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
rga = os.getenv('API_KEY')

# imports for the riot games api 
from riotwatcher import LolWatcher
watcher = LolWatcher(rga) 

# API routing variables 
region_routing_value = 'NA1'
ign = 'Yunikuna'



# Client is an object that represents a connection to Discord 
# Client handles events, trackes state, and interacts with Discord API 
intents = discord.Intents.default()
intents.members = True
intents.messages = True 
intents.guilds = True
# lets the bot respond back to messages 
intents.message_content = True
client = discord.Client(intents=intents)

# # this event will trigger when the initial connection from the bot --> server is established 
@client.event
async def on_ready():   # event handler is on_ready or AKA when connection is established bot --> server 
    for guild in client.guilds: 
        if guild.name == GUILD: 
            break
    print(
        f'{client.user} has connected to Discord!\n'
        f'{guild.name}(id: {guild.id})\n'  
    )

    # member_list = '\n - '.join([member.name for member in guild.members])
        # translated version of the line above 
    member_list = [] 
    for member in guild.members: 
        member_list.append(member.name)
    member_list = '\n - '.join(member_list)

    # output the people in the guild
    print(f'Guild Members:\n - {member_list}')  # for some reason it only outputs the bot name... EDIT: probably the premissions 
    print('Done!')

@client.event # tested and works
async def on_member_join(member): 
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, you are my favorite :3!'
    )


@client.event
async def on_message(message):
    # checks if the message of the user is a user and not a bot
    if message.author == client.user:
        return 

    if message.content == 'ping':
        response = 'pong'
        await message.channel.send(response)

    if message.content == 'test': 
        response = 'you suck'
        await message.channel.send(response)

    # This is currently working, but will need to find a way to determine user
    if message.content == 'tft':
        # we should grab user data as soon as the message is called 
        user_data = watcher.summoner.by_name(region_routing_value, ign)
        id = user_data['id']
        
        url = f'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{id}'
        headers = {"X-Riot-Token" : rga}

        response = requests.get(url, headers=headers)

        if response.status_code == 200: 
            data = response.json() 
            entry = data[0]
            player_tier = entry['tier']
            player_rank = entry['rank']

            print('Your current rank is ' + player_tier + ' ' + player_rank)
            # await message.channel.send('Your current rank is ' + player_tier + ' ' + player_rank)
            await message.channel.send('Your current rank is ' + player_tier + ' ' + player_rank)

        else: 
            print(f'Error: {response.status_code}') 
            # await message.channel.send(f'Error: {response.status_code}') 
            await message.channel.send('test1')



# @client.event
# async def on_Rank(message): 
#     # checks if the message of the user is actually a USER and not BOT 
#     if message.author == client.user: 
#         return 
    
#     if message.content == 'z': 
#         # we should grab user data as soon as the message is called 
#         user_data = watcher.summoner.by_name(region_routing_value, ign)
#         id = user_data['id']
        
#         url = f'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{id}'
#         headers = {"X-Riot-Token" : rga}

#         response = requests.get(url, headers=headers)

#         if response.status_code == 200: 
#             data = response.json() 
#             entry = data[0]
#             player_tier = entry['tier']
#             player_rank = entry['rank']

#             print('Your current rank is ' + player_tier + ' ' + player_rank)
#             # await message.channel.send('Your current rank is ' + player_tier + ' ' + player_rank)
#             await message.channel.send('test')

#         else: 
#             print(f'Error: {response.status_code}') 
#             # await message.channel.send(f'Error: {response.status_code}') 
#             await message.channel.send('test1')
#         content = 'yes'
#         await message.channel.send(content)






client.run(TOKEN)