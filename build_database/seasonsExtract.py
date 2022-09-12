import requests
import json

startUrl = 'https://statsapi.web.nhl.com/api/v1/seasons/'
seasonsStart = 1967
seasonsEnd = 2022

seasonList = []

while seasonsStart < seasonsEnd:
    seasonStr = str(seasonsStart) + str(seasonsStart + 1)
    seasonList.append(int(seasonStr))
    seasonsStart += 1

urlList = []
for season in seasonList:
    urlList.append(startUrl +str(season))

urlList.pop(37) # no 20042005 season

seasons = {}
i = 0
for url in urlList:
    response = requests.get(url)
    seasonsJson = response.json()
    data = json.dumps(seasonsJson)
    seasonData = json.loads(data)

    seasonsData = seasonData['seasons'][0]

    seasonId = seasonsData['seasonId']
    seasonStartRegular = seasonsData['regularSeasonStartDate']
    seasonEndRegular = seasonsData['regularSeasonEndDate']
    seasonEndPost = seasonsData['seasonEndDate']
    numberOfGames = seasonsData['numberOfGames']
    tiesInUse = seasonsData['tiesInUse']

    seasonTable = {
                  'seasonId': seasonId,
                  'seasonStartRegular': seasonStartRegular,
                  'seasonEndRegular': seasonEndRegular,
                  'seasonStartPost': seasonEndRegular,
                  'seasonEndPost': seasonEndPost,
                  'numberOfGames': numberOfGames,
                  'tiesInUse': tiesInUse
                  }

    seasons.update({i: seasonTable})
    i += 1

seasonsOutput = json.dumps(seasons, indent = 6,  separators = (", ",":"), sort_keys = True)

seasonsOutputJson = 'seasons.json'

f = open(seasonsOutputJson, 'w') #use 'a' to append
f.write(seasonsOutput)
f.close()