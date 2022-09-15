import requests
import json

startUrl = 'https://statsapi.web.nhl.com/api/v1/teams'

startId = 1
url = startUrl + str(startId)
y = 0
teams = {}
while y < 1:
    response = requests.get(url)
    teamJson = response.json()
    data = json.dumps(teamJson)
    teamData = json.loads(data)

    teamsDict = teamData['teams'][0]   

    teamId = teamsDict['id']
    name = teamsDict['name'] 
    abbreviation = teamsDict['abbreviation']
    divisionId = teamsDict['division']['id']
    venue = teamsDict['venue']['name']
    city = teamsDict['venue']['city']
    location = teamsDict['locationName']
    active = teamsDict['active']

    team = {
            'teamId': teamId,
            'name': name,
            'abbreviation': abbreviation,
            'divisionId': divisionId,
            'venue': venue,
            'city': city,
            'location': location,
            'active': active
           }
    
    teams.update({startId: team})
    startId += 1


output = json.dumps(teams, indent = 6,  separators = (", ",":"), sort_keys = True)

outputJson = 'teamsAll.json'
f = open(outputJson, 'w') #use 'a' to append
f.write(output)
f.close()