import requests
import json
import time
from extractFxns import (gameInfo, gameResult,
                        listPlayers, listSkaters, listGoalies,
                        skaterStats, goalieStats)
startUrl = 'https://statsapi.web.nhl.com/api/v1/game/'
endUrl = '/feed/live'
year = 1967
game = 20001
url = startUrl + str(year) + '0' + str(game) + endUrl

def listSkaters(gameData, side):
    skaters = gameData['liveData']['boxscore']['teams'][side]['skaters']#int
    players = gameData['liveData']['boxscore']['teams'][side]['players']#str
    skatersIdList = [] #str
    skatersList = list(skaters) #int
    for Id in skatersList: #int
        playerId = players[Id]['person']['id'] #int
        skatersIdList.append(str('ID' + playerId)) #str
    return skatersList, skatersIdList #int, str 

while year < 2022:
    time.sleep(0.35)
    response = requests.get(url)
    gameJson = response.json()
    data = json.dumps(gameJson)
    gameData = json.loads(data)

    print(listPlayers(gameData, 'away'))




