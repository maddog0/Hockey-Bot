import discord
import logging
import json
import requests
import asyncio
from teams import *
from games import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('config.json') as config_file:
    data = json.load(config_file)
token = data['token']
messages = int(data['messages'])
logs = int(data['logs'])

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.bg_task = self.loop.create_task(self.morning_cleanup())
        self.gb_task = self.loop.create_task(self.update_scheduled_status())
        self.bg_task = self.loop.create_task(self.in_game_update())

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send("YO")

    #should be run once a day in the morning
    async def morning_cleanup(self):
        await self.wait_until_ready()
        channel = self.get_channel(int(logs))
        while not self.is_closed():
            try:
                update_team_details()
                await channel.send("team list and links updated")                
                update_next_game_info()
                await channel.send("next game info updated")
            except Exception as e:
                await channel.send("An error occured in monring_cleanup: " + str(e))
            await asyncio.sleep(43200)

    #should be run every 10 seconds while a game in the database is in progress (status 2-5)
    async def in_game_update(self):
        await self.wait_until_ready()        
        channel = self.get_channel(int(messages))
        while not self.is_closed():
            try:
                if is_game_live() == True:
                    for message in check_game_updates():
                        await channel.send(message.upper())
                    for message in update_finished_games():
                        await channel.send(message.upper())
                    remove_complete()
                    await asyncio.sleep(1)
                else:
                    for message in update_finished_games():
                        await channel.send(message.upper())                      
                    remove_complete()
                    await asyncio.sleep(1800)
            except Exception as e:
                print("An error occured in Hockey_Bot.py in game update: "+str(e))

    async def update_scheduled_status(self):
        await self.wait_until_ready()
        while not self.is_closed():
            update_scheduled_games()
            await asyncio.sleep(1800)

client = MyClient()
client.run(token)
