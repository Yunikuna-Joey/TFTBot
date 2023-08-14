# imports for discord bot
import os
import random
import discord
import requests 

# will help with restructuring bot commands (everything client.event --> bot.event)
from discord.ext import commands


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
## this line of code is old  --> replaced with the next line underneath this 
# client = discord.Client(intents=intents)

# replaced with 
bot = commands.Bot(command_prefix='!', intents=intents)

# # this event will trigger when the initial connection from the bot --> server is established 
@bot.event
async def on_ready():   # event handler is on_ready or AKA when connection is established bot --> server 
    for guild in bot.guilds: 
        if guild.name == GUILD: 
            break
    print(
        f'{bot.user} has connected to Discord!\n'
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

@bot.event # tested and works
async def on_member_join(member): 
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, you are my favorite :3!'
    )

# to use commands we will reference the prefix plus the function name 
@bot.command() 
async def ping(ctx):
    await ctx.send('pong')

@bot.command() 
async def tftrank(ctx, arg_ign): 
    # grab the information about the ign that is being passed in the argument
    user_data = watcher.summoner.by_name(region_routing_value, arg_ign)
    id = user_data['id']

    # API call here
    url = f'https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{id}' 
    headers = {'X-Riot-Token' : rga}
    response = requests.get(url, headers=headers)

    # if we get a successful http code
    if response.status_code == 200: 
        data = response.json()
        entry = data[0]
        player_tier = entry['tier']
        player_rank = entry['rank']
        player_lp = entry['leaguePoints']

        # debug (ensures that the call was made)
        print('Ran tft rank command')
        # outputs into the discord channel 
        await ctx.send('Your current TFT rank is ' + player_tier + ' ' + player_rank + '\n' + 'LP: ' + str(player_lp)) 
    
    else: 
        print(f'Error: {response.status_code}')
        # outputs into the discord channel 
        await ctx.send(f'Error: {response.status_code}')

@bot.command() 
async def tftstatus(ctx): 
    # API call 
    url = f'https://na1.api.riotgames.com/tft/status/v1/platform-data?api_key=' + rga
    headers = {'X-Riot-Token': rga} 

    response = requests.get(url, headers=headers)
    
    # successful http code 
    if response.status_code == 200: 
        data = response.json()
        print('Ran tft status command')

        # should have the output 'North America' 
        region = data['name']

        # gives access to status and issue content
        maint_key = data['maintenances'][0]
        # should be in_progress 
        status = maint_key['maintenance_status']

        # gives access to the specific issue of maintenance
        issue_content = maint_key['titles'][0]
        # should be the NAME of issue 
        issue_name = issue_content['content']

        await ctx.send('Maintenance Region: ' +  region + '\n' + 
                       'Maintenance Status: ' + status + '\n' + 
                       'Maintenance Issue: ' + issue_name)
        
        


    
    else: 
        print(f'Error code: {response.status_code}')

bot.run(TOKEN)