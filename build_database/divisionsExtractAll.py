import requests
import json

startUrl = 'https://statsapi.web.nhl.com/api/v1/divisions/'
startId = 1

url = startUrl + str(startId)
y = 0
divisions = {}
while y < 1:
    response = requests.get(url)
    divJson = response.json()
    data = json.dumps(divJson)
    divData = json.loads(data)

    if 'divisions' in divData and divData['divisions'] != []:
        div = divData['divisions'][0]

        id = div['id']
        print(id)
        name = div['name'] 
        abbreviation = div['abbreviation']
        conferenceId = div['id']
        active = div['active']

        division = {
                    'id': id,
                    'name': name,
                    'abbreviation': abbreviation,
                    'conferenceId': conferenceId,
                    'active': active
                    }
        
        divisions.update({id: division})
        startId += 1
        url = startUrl + str(startId)

    else:
        y += 1

output = json.dumps(divisions, indent = 6,  separators = (", ",":"), sort_keys = True)
#print(output)

outputJson = 'divisionsAll.json'
f = open(outputJson, 'w') #use 'a' to append
f.write(output)
f.close()