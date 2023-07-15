import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Client is an object that represents a connection to Discord 
# Client handles events, trackes state, and interacts with Discord API 
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# this event will trigger when the initial connection from the bot --> server is established 
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

@client.event # this has not been tested, it should dm the person that just joined the server 
async def on_member_join(member): 
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, you are my favorite :3!'
    )

# if the bot cannot see other members in the server, it cannot collect messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == 'ping':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)


    

client.run(TOKEN)