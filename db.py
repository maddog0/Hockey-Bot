from pymongo import MongoClient
import json
from pprint import pprint

with open('config.json') as config_file:
    data = json.load(config_file)

password = data['password']

client = MongoClient(password)
db = client.Hockey

def update_team(team,id):
    try:
        db.teams.replace_one(
            {"_id" : id},
            team,
            upsert= True)
    except Exception as e:
        raise Exception("An Error occured: " + str(e))

def get_game_links():
    links = db.teams.distinct("link", { "link": {"$ne" : None}})
    return links

def update_game(game,id):
    try:
        db.games.replace_one(
            {"_id" : id},
            game,
            upsert=True)
    except Exception as e:
        raise Exception("An Error occured in game update: " + str(e))

def remove_game():
    try:
        db.games.delete_many({"status": "7"})
    except Exception as e:
        raise Exception("Could not remove game: " + str(e))

def get_goals(id):
    try:
        goals = db.games.findOne({"_id" : id},
                                 {"goals": 1},{"_id": 0})
        return goals
    except Exception as e:
        raise Exception("Could not get goals info: " + str(e))
