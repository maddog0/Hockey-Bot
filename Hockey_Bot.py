import discord
import logging
import json
import requests
import asyncio
import traceback
from teams import *
from games import *
from discord.utils import find
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('config.json') as config_file:
    data = json.load(config_file)
token = data['token']
logs = int(data['logs'])

prefix = '!'
bot = commands.Bot(command_prefix=prefix)
bot.load_extension("cogs.prefrencescog")
bot.load_extension("cogs.gamecog")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.bg_task = bot.loop.create_task(morning_cleanup())
    bot.gb_task = bot.loop.create_task(update_scheduled_status())
    bot.bg_task = bot.loop.create_task(in_game_update())

@bot.event
async def on_guild_join(guild):
    hockey = find(lambda m: m.name == 'hockey', guild.text_channels)
    sports = find(lambda m: m.name == 'sports', guild.text_channels)
    general = find(lambda m: m.name == 'general', guild.text_channels)
    id = guild.id
    all_games = False
    playoffs = True
    liked_teams = []
    messages = None
    if hockey and hockey.permissions_for(guild.me).send_messages:
        messages = hockey.id
        await messages.send
    elif sports and sports.permissions_for(guild.me).send_messages:
        messages = sports.id
    elif general and general.permissions_for(guild.me).send_messages:
        messages = general.id
    else:
        print('no valid channel')
    server = {
        '_id' : id,
        'messages' : messages,
        'all_games' : all_games,
        'playoffs' : playoffs,
        'liked_teams' : liked_teams
        }
    try:
        insert_server(server,id)
    except Exception as e:
        print('An error occured setting up a new server: ' + str(e))

@bot.event                                               
async def on_guild_remove(guild):
    id = guild.id
    try:
        remove_server(id)
    except Exception as e:
        print('An error occured removing a server: ' + str(e))

#should be run once a day in the morning
async def morning_cleanup():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(logs))
    while not bot.is_closed():
        try:
            update_team_details()
            await channel.send("team list and links updated")                
            update_next_game_info()
            await channel.send("next game info updated")
            remove_complete()
        except Exception as e:
            await channel.send("An error occured in monring_cleanup: " + str(e))
        await asyncio.sleep(43200)

#should be run every 10 seconds while a game in the database is in progress (status 2-5)
async def in_game_update():
    await bot.wait_until_ready()        
    channels = get_channels()
    while not bot.is_closed():
        try:
            if is_game_live() == True:
                for message in check_game_updates():
                    for channel in channels:
                        messages = bot.get_channel(channel["messages"])
                        await messages.send(message.upper())
                for message in update_finished_games():
                    for channel in channels:
                        messages = bot.get_channel(channel["messages"])
                        await messages.send(message.upper())
                remove_complete()
                await asyncio.sleep(1)
            else:
                for message in update_finished_games():
                    for channel in channels:
                        messages = bot.get_channel(channel["messages"])
                        await messages.send(message.upper())                      
                await asyncio.sleep(1800)
        except Exception as e:
            print("An error occured in Hockey_Bot.py in game update: "+str(e))

async def update_scheduled_status():
    await bot.wait_until_ready()
    while not bot.is_closed():
        update_scheduled_games()
        await asyncio.sleep(1800)

bot.run(token)
