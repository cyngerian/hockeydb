from turtle import position, window_height
import requests
import json
import csv

startUrl = 'https://statsapi.web.nhl.com/api/v1/people/'
urlList = []

with open('gamePlayerList.csv') as csvfile:
    reader = csv.reader(csvfile)
    playerListRead = list(reader)

playerList = playerListRead[0]

for player in playerList:
    urlList.append(startUrl + player)

players = {}
i = 1 
for url in urlList:
    response = requests.get(url)
    playerJson = response.json()
    data = json.dumps(playerJson)
    urlData = json.loads(data)

    playerData = urlData['people'][0]
    print(playerData['id'])

    if 'primaryNumber' in playerData:
        player = {
                'id': playerData['id'],
                'namefirst': playerData['firstName'],
                'nameLast': playerData['lastName'],
                'primaryNumber': playerData['primaryNumber'],
                'birthdate': playerData['birthDate'],
                'birthCity ': playerData['birthCity'],
                'birthCountry': playerData['birthCountry'],
                'nationality': playerData['nationality'],
                'height': playerData['height'],
                'weight': playerData['weight'],
                'shootsCatches': playerData['shootsCatches'],
                'position': playerData['primaryPosition']['abbreviation'],
                'active': playerData['active'],
                }
        
    else:
        player = {
                'id': playerData['id'],
                'namefirst': playerData['firstName'],
                'nameLast': playerData['lastName'],
                'birthdate': playerData['birthDate'],
                'birthCity ': playerData['birthCity'],
                'birthCountry': playerData['birthCountry'],
                'nationality': playerData['nationality'],
                'height': playerData['height'],
                'weight': playerData['weight'],
                'shootsCatches': playerData['shootsCatches'],
                'position': playerData['primaryPosition']['abbreviation'],
                'active': playerData['active'],
                }
        
    players.update({i: player})
    i += 1
    #print(eventIdx)

output = json.dumps(players, indent = 6,  separators = (", ",":"), sort_keys = True)
#print(output)

outputJson = 'players.json'
f = open(outputJson, 'w') #use 'a' to append
f.write(output)
f.close()