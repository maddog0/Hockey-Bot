import requests
from db import *

prefix = "https://statsapi.web.nhl.com"

#run as part of update everything, updates the data for all upcoming games
def update_next_game_info():
    links = get_next_game_links()
    for suffix in links:
        response = requests.get(prefix+suffix)
        gameData = response.json()
        id = gameData["gamePk"]
        goals = gameData["liveData"]["plays"]["scoringPlays"]
        game = {
            '_id' : id,
            'goals' : goals,
            'link' : gameData["link"],
            'start' : gameData["gameData"]["datetime"]["dateTime"],
            'status' : gameData["gameData"]["status"]["statusCode"],
            'home' : gameData["gameData"]["teams"]["home"]["name"],
            'homeScore' : gameData["liveData"]["linescore"]["teams"]["home"]["goals"],
            'homeTriCode' : gameData["gameData"]["teams"]["home"]["triCode"],
            'homeTeamName' : gameData["gameData"]["teams"]["home"]["teamName"],
            'homeTeamLocation' : gameData["gameData"]["teams"]["home"]["locationName"],
            'away' : gameData["gameData"]["teams"]["away"]["name"],
            'awayScore' : gameData["liveData"]["linescore"]["teams"]["away"]["goals"],
            'awayTriCode' : gameData["gameData"]["teams"]["away"]["triCode"],
            'awayTeamName' : gameData["gameData"]["teams"]["away"]["teamName"],
            'awayTeamLocation' : gameData["gameData"]["teams"]["away"]["locationName"],
            'goaldetails': []
        }
        try:
            update_game(game,id)
        except Exception as e:
            raise Exception("An error occured in games.py udate_game_info: " + str(e))

#removes games that are totally complete (status 7)
def remove_complete():
    try:
        remove_games()
    except Exception as e:
        raise Exception("An error occured in games.py remove_complete: " + str(e))

#takes in some form of identifying information and pulls back details on the game that team is involved in if there are any
#Identification data can be the team name, the full name, the tricode, or the city the team is based in
def find_game_involving_team(identifier):
    return get_game_by_team(identifier)

#returns true if a game is currently live (state 3 4 or 5) returns false otherwise    
def is_game_live():
    try:
        if len(get_live_games()) != 0:
            return True
        else:
            return False
    except Exception as e:
        raise Exception("An error occured in games.py is_game_live: " +str(e))

def update_scheduled_games():
    games = get_scheduled_games()
    for game in games:
        response = requests.get(prefix+game["link"])
        gameData = response.json()
        game["status"] = gameData["gameData"]["status"]["statusCode"]
        update_game(game,game["_id"])

def check_game_updates():
    games = get_live_games()
    messages = []
    for game in games:        
        response = requests.get(prefix+game["link"])
        gameData = response.json()
        home = gameData["gameData"]["teams"]["home"]["triCode"]
        away = gameData["gameData"]["teams"]["away"]["triCode"]
        new_goals = gameData["liveData"]["plays"]["scoringPlays"]
        old_goals = game["goals"]
        goals_scored = len(new_goals)-len(old_goals)
        if goals_scored>0:
            new_goals=new_goals[-goals_scored:]
            goalDetails = get_goal_details(new_goals,gameData)
            update_live_game_data(game,gameData,goalDetails)
            for goal in goalDetails:
                messages.append(parse_goal(goal,home,away))
        if goals_scored<0:
            goalDetails = get_goal_details(new_goals,gameData)
            update_live_game_data(game,gameData,goalDetails)
            messages.append("a goal was overturned")
        else:
            update_live_game_data(game,gameData,game["goaldetails"])
    return messages
    
def update_live_game_data(game,gameData,goalDetails):
    game["goals"] = gameData["liveData"]["plays"]["scoringPlays"]
    game["status"] = gameData["gameData"]["status"]["statusCode"]
    game["goaldetails"] = goalDetails
    game["homeScore"] = gameData["liveData"]["linescore"]["teams"]["home"]["goals"]
    game["awayScore"] = gameData["liveData"]["linescore"]["teams"]["away"]["goals"]
    update_game(game,game["_id"])
    
    
def get_goal_details(goals,gameData):
    details = []
    for goal in goals:
        details.append(gameData["liveData"]["plays"]["allPlays"][goal])
    return details

def update_finished_games():
    games = get_finished_games()
    messages = []
    for game in games:
        response = requests.get(prefix+game["link"])
        gameData= response.json()
        home = gameData["gameData"]["teams"]["home"]["triCode"]
        home_score = gameData["liveData"]["linescore"]["teams"]["home"]["goals"]
        away = gameData["gameData"]["teams"]["away"]["triCode"]
        away_score = gameData["liveData"]["linescore"]["teams"]["away"]["goals"]
        game["status"] = gameData["gameData"]["status"]["statusCode"]
        update_game(game,game["_id"])
        message = "game over Final Score: {0}-{1}  {2}-{3}".format(home,home_score,away,away_score)
        messages.append(message)
    return messages
        
        
def parse_goal(goal,home,away):
    scorer = goal["result"]["description"]
    home_score = goal["about"]["goals"]["home"]
    away_score = goal["about"]["goals"]["away"]
    time = goal["about"]["periodTime"]
    period = goal["about"]["ordinalNum"]
    message = '''goal!!!! scored by: {0}
{1}-{2}  {3}-{4}
time of the goal {5} of the {6} period'''.format(scorer,home,home_score,away,away_score,time,period)
    return message


