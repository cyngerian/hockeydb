import requests
import json

startUrl = 'https://statsapi.web.nhl.com/api/v1/game/'
endUrl = '/feed/live'
gameID = 2021020001 # first game of regular season

game = gameID
gameList = []


while game < 2021020010: # max number of games per 32 team season
    gameList.append(game)
    game += 1

urlList = []
for game in gameList:
    urlList.append(startUrl +str(game) + endUrl )

games = {}
gameResults = {}
gamePlayerList = []
i = 0
for url in urlList:
    response = requests.get(url)
    gameJson = response.json()
    data = json.dumps(gameJson)
    gameData = json.loads(data)

    # common values
    gameId = gameData['gamePk']

    # CODE ERASED. SEE PROD
    
    # player stats

    # away team player stats
    awayPlayers = gameData['liveData']['boxscore']['teams']['away']['players']
    awayPlayerList = []
    awayPlayerStats = {}
    for player in awayPlayers:
        playerIdList = list(awayPlayers)

    for Id in playerIdList:
        awayPlayerId = awayPlayers[Id]['person']['id']
        awayPlayerList.append(awayPlayerId)
        

        if 'skaterStats' in awayPlayers[Id]['stats']:
            awaySkaterStats = awayPlayers[Id]['stats']['skaterStats']
            awayPlayerStats = {
                        'gameId': gameId,
                        'playerId': awayPlayerId,
                        'goals': awaySkaterStats['goals'],
                        'assists': awaySkaterStats['assists'],
                        'hits': awaySkaterStats['hits'],
                        'shotsOnGoal': awaySkaterStats['shots'],
                        'penaltyMin': awaySkaterStats['penaltyMinutes'],
                        'blocks': awaySkaterStats['blocked'],
                        'timeOnIce': awaySkaterStats['timeOnIce'],
                        'powerPlayTOI': awaySkaterStats['powerPlayTimeOnIce'],
                        'penaltyKillTOI': awaySkaterStats['shortHandedTimeOnIce'],
                        'faceoffsTaken': awaySkaterStats['faceoffTaken'],
                        'faceoffsWon': awaySkaterStats['faceOffWins']
                        }
            print(awayPlayerStats)


    for player in awayPlayerList:
        if player not in gamePlayerList:
            gamePlayerList.append(player)

    # home team player stats
    homePlayers = gameData['liveData']['boxscore']['teams']['home']['players']
    homePlayerList = []
    for player in homePlayers:
        playerIdList = list(homePlayers)

    for Id in playerIdList:
        homePlayerId = homePlayers[Id]['person']['id']
        homePlayerList.append(homePlayerId)

    for player in homePlayerList:
        if player not in gamePlayerList:
            gamePlayerList.append(player)


    i += 1

print(gamePlayerList)
