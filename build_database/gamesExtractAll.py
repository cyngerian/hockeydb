import requests
import json

startUrl = 'https://statsapi.web.nhl.com/api/v1/game/'
endUrl = '/feed/live'
gameID = 2021020001 # first game of regular season

game = gameID
gameList = []

print(gameList)
while game < 2021021312: # max number of games per 32 team season
    gameList.append(game)
    game += 1

urlList = []
for game in gameList:
    urlList.append(startUrl +str(game) + endUrl )

games = {}
gameResults = {}
i = 0
for url in urlList:
    response = requests.get(url)
    gameJson = response.json()
    data = json.dumps(gameJson)
    gameData = json.loads(data)

    # common values
    gameId = gameData['gamePk']

    # values for games
    season = gameData['gameData']['game']['season']
    dateTime = gameData['gameData']['datetime']['dateTime']
    homeTeam = gameData['gameData']['teams']['home']['id']
    awayTeam = gameData['gameData']['teams']['away']['id']
    status = gameData['gameData']['status']['detailedState']

    gameTable = {
                'gameId': gameId,
                'season': season,
                'dateTime': dateTime,
                'homeTeam': homeTeam,
                'awayTeam' : awayTeam,
                'status': status
                }

    # values for gameResults
    homeTeamScore = gameData['liveData']['linescore']['teams']['home']['goals']
    awayTeamScore = gameData['liveData']['linescore']['teams']['away']['goals']
    endType = gameData['liveData']['linescore']['currentPeriod']

    gameResultsTable = {
                'gameId': gameId,
                'homeTeamScore': homeTeamScore,
                'awayTeamScore': awayTeamScore,
                'endType': endType
                }

    games.update({i: gameTable})
    gameResults.update({i: gameResultsTable})
    i += 1

gamesOutput = json.dumps(games, indent = 6,  separators = (", ",":"), sort_keys = True)
gameResultsOutput = json.dumps(gameResults, indent = 6,  separators = (", ",":"), sort_keys = True)

gamesOutputJson = 'games.json'
gameResultsOutputJson = 'gameResults.json'
f = open(gamesOutputJson, 'w') #use 'a' to append
f.write(gamesOutput)
f.close()
f = open(gameResultsOutputJson, 'w') #use 'a' to append
f.write(gameResultsOutput)
f.close()