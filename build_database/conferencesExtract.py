import requests
import json

url = 'https://statsapi.web.nhl.com/api/v1/conferences'

response = requests.get(url)

confJson = response.json()
data = json.dumps(confJson)
confData = json.loads(data)

conferences = {}
confId = 0

for confId in range(len(confData['conferences'])):
    confs = confData['conferences'][confId]   


    id = confs['id']
    name = confs['name'] 
    abbreviation = confs['abbreviation']
    shortName = confs['shortName']
    active = confs['active']

    conference = {
                   'id': id,
                   'name': name,
                   'abbreviation': abbreviation,
                   'shortName': shortName,
                   'active': active
                  }
    
    conferences.update({confId: conference})
    confId += 1
    #print(eventIdx)

output = json.dumps(conferences, indent = 6,  separators = (", ",":"), sort_keys = True)
print(output)

outputJson = 'conferences.json'
f = open(outputJson, 'w') #use 'a' to append
f.write(output)
f.close()