import discord
import logging
import json
import requests
import sched, time
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
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        message_channel = discord.Client.get_channel(self,messages)
        logs_channel = discord.Client.get_channel(self,logs)
        s = sched.scheduler(time.time, time.sleep)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await update_everything(channel)

#should be run once a day in the morning
    async def update_everything(channel)
        try:
            update_team_details()
            await logs_channel.send("team list and links updated")
            update_game_info()
            await logs_channel.send("game details updated")
            remove_complete()
            await logs_channel.send("removed completed games")
        except Exception as e:
            await logs_channel.send(e)
        s.enter(
            
#should be run every 10 seconds while a game in the database is in progress (not status 1 or 7)
    async def in_game_update():
        #todo implement

client = MyClient()
client.run(token)
