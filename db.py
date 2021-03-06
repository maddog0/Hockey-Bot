from pymongo import MongoClient
import json
from pprint import pprint

with open('config.json') as config_file:
    data = json.load(config_file)

password = data['password']

client = MongoClient(password)
db = client.Hockey

def insert_server(server,id):
    try:
        db.servers.replace_one(
            {"_id": id},
            server,
            upsert = True)
    except Exception as e:
        raise Exception("An error occured in db.py insert_server: " + str(e))
    
def remove_server(id):
    try:
        db.servers.delete_many({"_id":id})
    except Exception as e:
        raise Exception("An error occured in db.py remove_server: " + str(e))

def update_server(id, key, value):
    query = {"_id": id}
    newvalue = {"$set": {key:value}}
    db.servers.update_one(query,newvalue)

def get_likedTeams(id):
    cursor = db.servers.find_one({"_id" : id},{"_id": 0,"liked_teams":1})
    return cursor

def get_channels():
    try:
        cursor = list(db.servers.find({},{"_id": 0,"messages": 1}))
        return cursor
    except Exception as e:
        raise Exception("An error occured in db.py get_channels: " + str(e))
                      

#work involving teams database
def update_team(team,id):
    try:
        db.teams.replace_one(
            {"_id" : id},
            team,
            upsert= True)
    except Exception as e:
        raise Exception("An error occured in db.py update_team: " + str(e))

def get_next_game_links():
    try:
        links = db.teams.distinct("link", { "link": {"$ne" : None}})
        return links
    except Exception as e:
        raise Exception("An error occured in db.py get_next_game_links: " + str(e))

def get_team(identifier):
    try:
        cursor = db.teams.find_one({"$or": [{"name": identifier},
                                            {"abbreviation": identifier},
                                            {"teamName": identifier},
                                            {"shortName": identifier}]})
        return cursor
    except Exception as e:
        raise Exception("An error occured in db.py get_team: " + str(e))

#functions involving games database
def update_game(game,id):
    try:
        db.games.replace_one(
            {"_id" : id},
            game,
            upsert=True)
    except Exception as e:
        raise Exception("An error occured in db.py update_game: " + str(e))

def remove_games():
    try:
        db.games.delete_many({"$or" : [{"status": "7"},
                                       {"status": "8"}]})
    except Exception as e:
        raise Exception("An error occured in db.py remove_games: " + str(e))

def get_goals_in_game(id):
    try:
        goals = db.games.find_one({"_id": id},{"_id": 0,"goals":1})
        return goals
    except Exception as e:
        raise Exception("An error occured in db.py get_goals_in_game: " + str(e))

def get_game_by_team(team_identifier):
    try:
        cursor = db.games.find_one({"$or": [{"homeTriCode": team_identifier},
                                            {"home": team_identifier},
                                            {"homeTeamName": team_identifier},
                                            {"homeTeamLocation": team_identifier},
                                            {"away": team_identifier},
                                            {"awayTriCode": team_identifier},
                                            {"awayTeamName": team_identifier},
                                            {"awayTeamLocation": team_identifier}]})
        return cursor
    except Exception as e:
        raise Exception("An error occured in db.py get_game_by_team: " + str(e))

def get_game_by_id(id):
    try:
        cursor = db.games.find_one({"_id": id})
        return cursor
    except Exception as e:
        raise Exception("An error occured in db.py get_game_by_id: " + str(e))

#returns a list of all currently live games
def get_live_games():
    try:
        cursor = list(db.games.find({"$or": [{"status":'2'},
                                  {"status":'3'},
                                  {"status":'4'},
                                  {"status":'5'},
                                  {"status":'6'}]}))
        return cursor
    except Exception as e:
        raise Exception("An error occured in db.py get_live_games: " + str(e))

#returns a list of all games that are finished
def get_finished_games():
    try:
        cursor = list(db.games.find({"status" : '7'}))
        return cursor
    except Exception as e:
        raise Exception("An error occured in db.py get_finished_games: " + str(e))

def get_scheduled_games():
    try:
        cursor = list(db.games.find({"status" : '1'}))
        return cursor
    except Exception as e:
        raise Exception("An error occured in db.py get_all_games: " + str(e))
