import discord
import json
import requests
from pymongo import MongoClient

with open('config.json') as config_file:
    data = json.load(config_file)
token = data['token']
password = data['password']

client = MongoClient("mongodb+srv://wcallanan:"+password+"@hockeybot-da9pp.mongodb.net/test?retryWrites=true")
db = client.Hockey

#data = response.json()["liveData"]["plays"]["scoringPlays"]
prefix = "https://statsapi.web.nhl.com/api/v1/"

def update_team_details():
    suffix = "teams/?expand=team.schedule.next"
    response = requests.get(prefix+suffix)
    teams = response.json()["teams"]
    for x in teams:
        id = x["id"]
        team = {
            '_id' : id,            
            'name' : x["name"],
            'abbreviation' : x["abbreviation"],
            'teamName' : x["teamName"],
            'shortName' : x["shortName"],
            'link' : get_link(id)
        }
        try:
            db.teams.replace_one(
                {"_id" : id},
                team,
                upsert= True)
        except(e):
            print(e)
        
    print('finished')
        

def get_link(id):
    suffix = "teams/"+str(id)+"?expand=team.schedule.next"
    response = requests.get(prefix+suffix)
    link = response.json()["teams"][0]
    link = link.get("nextGameSchedule")
    if link == None:
        return link
    else:
        link = response.json()["teams"][0]["nextGameSchedule"]["dates"][0]["games"][0]["link"]
        return link
              
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        update_team_details()

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('hello to you')



client = MyClient()
client.run(token)
