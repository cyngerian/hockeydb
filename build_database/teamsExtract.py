import requests
import json

url = 'https://statsapi.web.nhl.com/api/v1/teams'

response = requests.get(url)

teamJson = response.json()
data = json.dumps(teamJson)
teamData = json.loads(data)

teams = {}
i = 0

for i in range(len(teamData['teams'])):
    teamsDict = teamData['teams'][i]   

    teamId = teamsDict['id']
    name = teamsDict['name'] 
    abbreviation = teamsDict['abbreviation']
    divisionId = teamsDict['division']['id']
    venue = teamsDict['venue']['name']
    city = teamsDict['venue']['city']
    location = teamsDict['locationName']

    team = {
            'teamId': teamId,
            'name': name,
            'abbreviation': abbreviation,
            'divisionId': divisionId,
            'venue': venue,
            'city': city,
            'location': location
           }
    
    teams.update({i: team})
    i += 1
    #print(eventIdx)

output = json.dumps(teams, indent = 6,  separators = (", ",":"), sort_keys = True)
#print(output)

outputJson = 'teams.json'
f = open(outputJson, 'w') #use 'a' to append
f.write(output)
f.close()