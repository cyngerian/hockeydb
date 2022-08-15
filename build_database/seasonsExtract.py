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
# print(urlList)

seasons = {}
for url in urlList:
    response = requests.get(url)
    seasonsJson = response.json()
    data = json.dumps(seasonsJson)
    seasonsData = json.loads(data)