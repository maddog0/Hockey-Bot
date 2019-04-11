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

        self.bg_task = self.loop.create_task(self.in_game_update())
        self.bg_task = self.loop.create_task(self.update_everything())        

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send("YO")

    #should be run once a day in the morning
    async def update_everything(self):
        await self.wait_until_ready()
        channel = self.get_channel(int(logs))
        while not self.is_closed():
            try:
                update_game_info()
                await channel.send("game details updated")
                remove_complete()
                await channel.send("removed completed games")
                update_team_details()
                await channel.send("team list and links updated")
            except Exception as e:
                await channel.send(e)
            await asyncio.sleep(200)

    #should be run every 10 seconds while a game in the database is in progress (not status 1 or 7)
    async def in_game_update(self):
        await self.wait_until_ready()
        channel = self.get_channel(int(messages))
        while not self.is_closed():
            if is_game_live() == True:
                await channel.send("live game")
                await asyncio.sleep(10)
            else:
                await channel.send("no live game")
                await asyncio.sleep(1800)

client = MyClient()
client.run(token)
