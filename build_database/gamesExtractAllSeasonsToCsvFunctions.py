import requests
import json
import time
from extractFxns import (getGameInfo, getGameResult,
                        listSkaters, listGoalies,
                        getSkaterStats, getGoalieStats)

startUrl = 'https://statsapi.web.nhl.com/api/v1/game/'
endUrl = '/feed/live'
year = 1967
game = 20001
url = startUrl + str(year) + '0' + str(game) + endUrl

while year < 2022:
    time.sleep(0.35)
    response = requests.get(url)
    gameJson = response.json()
    data = json.dumps(gameJson)
    gameData = json.loads(data)

    if 'gamePk' in gameData:
        gameId = gameData['gamePk']

        print(getGameInfo(gameId, gameData))

        print(getGameResult(gameId, gameData))
        
        for Id in listSkaters(gameData, 'away'):
            print(getSkaterStats(gameId, gameData, 'away', Id))
        for Id in listGoalies(gameData, 'away'):
            print(getGoalieStats(gameId, gameData, 'away', Id))
        for Id in listSkaters(gameData, 'home'):
            print(getSkaterStats(gameId, gameData, 'home', Id))
        for Id in listGoalies(gameData, 'home'):
            print(getGoalieStats(gameId, gameData, 'home', Id))
        
        game += 1
        url = startUrl + str(year) + '0' + str(game) + endUrl

    else:
        game = 20001
        year += 1
        if year == 2004:
            year += 1
        url = startUrl + str(year) + '0' + str(game) + endUrl