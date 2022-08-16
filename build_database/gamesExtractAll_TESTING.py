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
gamePlayerStats = {}
gamePlayerList = []
awayPlayerStatsTable = {}

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
    j = 0
    for player in awayPlayers:
        playerIdList = list(awayPlayers)

    for Id in playerIdList:
        awayPlayerId = awayPlayers[Id]['person']['id']
        awayPlayerList.append(awayPlayerId)
        

        if 'skaterStats' in awayPlayers[Id]['stats']:
            awaySkaterStats = awayPlayers[Id]['stats']['skaterStats']
            awayPlayerStats = {
                        'gameId': gameId,
                        'team': gameData['liveData']['boxscore']['teams']['away']['team']['id'],
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
            awayPlayerStatsTable.update({j: awayPlayerStats})
            j += 1
    print(awayPlayerStatsTable)


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

        if 'skaterStats' in homePlayers[Id]['stats']:
            homeSkaterStats = homePlayers[Id]['stats']['skaterStats']
            homePlayerStats = {
                        'gameId': gameId,
                        'team': gameData['liveData']['boxscore']['teams']['away']['team']['id'],
                        'playerId': homePlayerId,
                        'goals': homeSkaterStats['goals'],
                        'assists': homeSkaterStats['assists'],
                        'hits': homeSkaterStats['hits'],
                        'shotsOnGoal': homeSkaterStats['shots'],
                        'penaltyMin': homeSkaterStats['penaltyMinutes'],
                        'blocks': homeSkaterStats['blocked'],
                        'timeOnIce': homeSkaterStats['timeOnIce'],
                        'powerPlayTOI': homeSkaterStats['powerPlayTimeOnIce'],
                        'penaltyKillTOI': homeSkaterStats['shortHandedTimeOnIce'],
                        'faceoffsTaken': homeSkaterStats['faceoffTaken'],
                        'faceoffsWon': homeSkaterStats['faceOffWins']
                        }

    for player in homePlayerList:
        if player not in gamePlayerList:
            gamePlayerList.append(player)

    #print(awayPlayerStats)

    #gamePlayerStatsTable = awayPlayerStats.update(homePlayerStats)
    #print(gamePlayerStatsTable)

    #gamePlayerStats.update({i: gamePlayerStatsTable})
    i += 1

#print(awayPlayerStats)
