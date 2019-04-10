import requests
from db import *

prefix = "https://statsapi.web.nhl.com"

def update_game_info():
    links = get_game_links()
    for suffix in links:
        response = requests.get(prefix+suffix)
        gameData = response.json()
        id = gameData["gamePk"]
        goals = gameData["liveData"]["plays"]["scoringPlays"]
        game = {
            '_id' : id,
            'goals' : goals,
            'start' : gameData["gameData"]["datetime"]["dateTime"],
            'status' : gameData["gameData"]["status"]["statusCode"],
            'home' : gameData["gameData"]["teams"]["home"]["name"],
            'away' : gameData["gameData"]["teams"]["away"]["name"]
        }
        try:
            update_game(game,id)
        except Exception as e:
            raise Exception(e)
    print('completed game update')

def remove_complete():
    remove_game()
    print('removed complete games')

def check_goal(old, new):
    if 
