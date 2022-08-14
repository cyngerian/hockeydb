import requests
import json

url = 'https://statsapi.web.nhl.com/api/v1/divisions'

response = requests.get(url)

divJson = response.json()
data = json.dumps(divJson)
divData = json.loads(data)

divisions = {}
divId = 0

for divId in range(len(divData['divisions'])):
    divs = divData['divisions'][divId]   


    id = divs['id']
    name = divs['name'] 
    abbreviation = divs['abbreviation']
    conferenceId = divs['conference']['id']
    active = divs['active']

    division = {
                   'id': id,
                   'name': name,
                   'abbreviation': abbreviation,
                   'conferenceId': conferenceId,
                   'active': active
                  }
    
    divisions.update({divId: division})
    divId += 1
    #print(eventIdx)

output = json.dumps(divisions, indent = 6,  separators = (", ",":"), sort_keys = True)
#print(output)

outputJson = 'divisions.json'
f = open(outputJson, 'w') #use 'a' to append
f.write(output)
f.close()