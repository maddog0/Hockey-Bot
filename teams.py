import requests
from db import *

prefix = "https://statsapi.web.nhl.com"

def update_team_details():
    suffix = "/api/v1/teams/?expand=team.schedule.next"
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
            update_team(team,id)
        except Exception as e:
            raise Exception("An error occured in teams.py update_team_details: " + str(e))

def get_link(id):
    suffix = "/api/v1/teams/"+str(id)+"?expand=team.schedule.next"
    response = requests.get(prefix+suffix)
    link = response.json()["teams"][0]
    link = link.get("nextGameSchedule")
    if link == None:
        return link
    else:
        link = response.json()["teams"][0]["nextGameSchedule"]["dates"][0]["games"][0]["link"]
        return link

def find_team(identifier):
    return get_team(identifier)
