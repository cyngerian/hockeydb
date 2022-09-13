import requests
import json

startUrl = 'https://statsapi.web.nhl.com/api/v1/conferences/'
startId = 1

url = startUrl + str(startId)
y = 0
conferences = {}
while y < 1:
    response = requests.get(url)
    confJson = response.json()
    data = json.dumps(confJson)
    confData = json.loads(data)


    if 'conferences' in confData:
        conf = confData['conferences'][0]   

        id = conf['id']
        name = conf['name'] 
        abbreviation = conf['abbreviation']
        shortName = conf['shortName']
        active = conf['active']

        conference = {
                    'id': id,
                    'name': name,
                    'abbreviation': abbreviation,
                    'shortName': shortName,
                    'active': active
                    }
        
        conferences.update({id: conference})
        startId += 1
        url = startUrl + str(startId)
    
    else:
        y += 1

output = json.dumps(conferences, indent = 6,  separators = (", ",":"), sort_keys = True)

outputJson = 'conferencesAll.json'
f = open(outputJson, 'w') #use 'a' to append
f.write(output)
f.close()