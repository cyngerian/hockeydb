import requests
import json
import time
from skaterStatsFxns import skaterStatsDict, listPLayers

startUrl = 'https://statsapi.web.nhl.com/api/v1/game/'
endUrl = '/feed/live'
startYear = 1967
startGame = 20001
url = startUrl + str(startYear) + '0' + str(startGame) + endUrl



startYear = 1967
while startYear < 2022:
    time.sleep(0.35)
    response = requests.get(url)
    gameJson = response.json()
    data = json.dumps(gameJson)
    gameData = json.loads(data)

    if 'gamePk' in gameData:
        gameId = gameData['gamePk']

        for Id in listPLayers(gameData, 'away')[1]:
            print(skaterStatsDict(gameData, 'away', Id))

        for Id in listPLayers(gameData, 'home')[1]:
            print(skaterStatsDict(gameData, 'home', Id))
        
        startGame += 1
        url = startUrl + str(startYear) + '0' + str(startGame) + endUrl

    else:
        startGame = 20001
        startYear += 1
        if startYear == 2004:
            startYear += 1
        url = startUrl + str(startYear) + '0' + str(startGame) + endUrl