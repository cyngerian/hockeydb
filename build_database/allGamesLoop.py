import requests
import json
import pandas
import time

startUrl = 'https://statsapi.web.nhl.com/api/v1/game/'
endUrl = '/feed/live'
startYear = 1967
startGame = 20001
url = startUrl + str(startYear) + '0' + str(startGame) + endUrl

y = 0
gameUrlList = []

n = 0
runStartTime = time.time()

while startYear < 2022:
    response = requests.get(url)
    gameJson = response.json()
    data = json.dumps(gameJson)
    gameData = json.loads(data)

    time.sleep(0.25)


    if 'gamePk' in gameData:
        gameUrlList.append(url)
        startGame += 1
        url = startUrl + str(startYear) + '0' + str(startGame) + endUrl
        
        n += 1 
        currentTime = time.time()
        elapsed = "%.2f" % (currentTime - runStartTime)
        print(str(n) + '   ' + str(gameData['gamePk']) + '   ' + elapsed)

    else: 
        startGame = 20001
        startYear += 1
        if startYear == 2004:
            startYear += 1
        url = startUrl + str(startYear) + '0' + str(startGame) + endUrl

df = pandas.DataFrame(data={"urls": gameUrlList})

df.to_csv("./gameUrlList.csv", sep=',',index=False)