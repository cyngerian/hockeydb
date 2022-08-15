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

#print(seasonList)