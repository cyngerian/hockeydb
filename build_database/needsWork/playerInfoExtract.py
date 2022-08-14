import requests
import json

startUrl = 'https://statsapi.web.nhl.com/api/v1/people/'

# need to generate players list from game extract - 2022-08-14
with open('playerList.txt', 'r') as fp:
    playerList = json.load(fp)

urlList = []
for playerId in playerList:
    urlList.append(startUrl +str(playerId[2:]))

#print(urlList)
#urlList = ['https://statsapi.web.nhl.com/api/v1/people/8473463']
i = 0
playerInfo = {}
for url in urlList:

    response = requests.get(url)
    playerJson = response.json()
    data = json.dumps(playerJson)
    playerData = json.loads(data)

    player = playerData['people'][0]
    if 'primaryNumber' in player:
        playerTable = {
                        'playerId': player['id'],
                        'lastName': player['lastName'],
                        'firstName': player['firstName'],
                        'primaryNumber': player['primaryNumber'],
                        'birthDate': player['birthDate'],
                        #'currentAge': player['currentAge'],
                        'birthCity': player['birthCity'],
                        'birthCountry': player['birthCountry'],
                        'nationality': player['nationality'],
                        'height': player['height'],
                        'weight': player['weight'],
                        'shootsCatches': player['shootsCatches'],
                        #'currentTeamId': player['currentTeam']['id'],
                        'primaryPosition': player['primaryPosition']['code'],
                        }
    else: 
        playerTable = {
                        'playerId': player['id'],
                        'lastName': player['lastName'],
                        'firstName': player['firstName'],
                        'primaryNumber': 0,
                        'birthDate': player['birthDate'],
                        #'currentAge': player['currentAge'],
                        'birthCity': player['birthCity'],
                        'birthCountry': player['birthCountry'],
                        'nationality': player['nationality'],
                        'height': player['height'],
                        'weight': player['weight'],
                        'shootsCatches': player['shootsCatches'],
                        #'currentTeamId': player['currentTeam']['id'],
                        'primaryPosition': player['primaryPosition']['code'],
                        }

    print(i, ' - ', playerTable['playerId'], playerTable['firstName'], playerTable['lastName'])
    playerInfo.update({i:playerTable})
    i += 1

output = json.dumps(playerInfo, indent = 6,  separators = (", ",":"), sort_keys = False)
#print(output)

outputJson = 'playerInfo.json'
f = open(outputJson, 'w') #use 'a' to append
f.write(output)
f.close()