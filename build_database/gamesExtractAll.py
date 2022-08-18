import requests
import json
import csv

startUrl = 'https://statsapi.web.nhl.com/api/v1/game/'
endUrl = '/feed/live'
gameID = 2021020001 # first game of regular season

game = gameID
gameList = []

while game < 2021021313: # max number of games per 32 team season
    gameList.append(game)
    game += 1

urlList = []
for game in gameList:
    urlList.append(startUrl +str(game) + endUrl )

games = {}
gameResults = {}
gamePlayerStats = {}
gamePlayerList = []
playerStatsTable = {}

i = 0
j = 0
k = 0
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
    games.update({i: gameTable})
    i += 1

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
    gameResults.update({j: gameResultsTable})
    j += 1
    
    # player stats

    # away team player stats
    awayPlayers = gameData['liveData']['boxscore']['teams']['away']['players']
    awayPlayerList = []
    awayPlayerStats = {}
    awayPlayerIdList = list(awayPlayers)
    
    for Id in awayPlayerIdList:
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
        elif 'goalieStats' in awayPlayers[Id]['stats']:
            awayGoalieStats = awayPlayers[Id]['stats']['goalieStats']
            awayPlayerStats = {
                        'gameId': gameId,
                        'team': gameData['liveData']['boxscore']['teams']['away']['team']['id'],
                        'playerId': awayPlayerId,
                        'goals': awayGoalieStats['goals'],
                        'assists': awayGoalieStats['assists'],
                        'shotsFaced': awayGoalieStats['shots'],
                        'saves': awayGoalieStats['saves'],
                        'powerPlayShotsFaced': awayGoalieStats['powerPlayShotsAgainst'],
                        'powerplaySaves': awayGoalieStats['powerPlaySaves'],
                        'timeOnIce': awayGoalieStats['timeOnIce'],
                        'penaltyMin': awayGoalieStats['pim'],
                        'decision': awayGoalieStats['decision']
                        }
        else: awayPlayerStats = {}

        playerStatsTable.update({k: awayPlayerStats})
        k += 1

    for player in awayPlayerList:
        if player not in gamePlayerList:
            gamePlayerList.append(player)

    # home team player stats
    homePlayers = gameData['liveData']['boxscore']['teams']['home']['players']
    homePlayerList = []
    homePlayerStats = {}
    homePlayerIdList = list(homePlayers)

    for Id in homePlayerIdList:
        homePlayerId = homePlayers[Id]['person']['id']
        homePlayerList.append(homePlayerId)

        if 'skaterStats' in homePlayers[Id]['stats']:
            homeSkaterStats = homePlayers[Id]['stats']['skaterStats']
            homePlayerStats = {
                        'gameId': gameId,
                        'team': gameData['liveData']['boxscore']['teams']['home']['team']['id'],
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
        elif 'goalieStats' in homePlayers[Id]['stats']:
            homeGoalieStats = homePlayers[Id]['stats']['goalieStats']
            homePlayerStats = {
                        'gameId': gameId,
                        'team': gameData['liveData']['boxscore']['teams']['home']['team']['id'],
                        'playerId': homePlayerId,
                        'goals': homeGoalieStats['goals'],
                        'assists': homeGoalieStats['assists'],
                        'shotsFaced': homeGoalieStats['shots'],
                        'saves': homeGoalieStats['saves'],
                        'powerPlayShotsFaced': homeGoalieStats['powerPlayShotsAgainst'],
                        'powerplaySaves': homeGoalieStats['powerPlaySaves'],
                        'timeOnIce': homeGoalieStats['timeOnIce'],
                        'penaltyMin': homeGoalieStats['pim'],
                        'decision': homeGoalieStats['decision']
                        }
        else: homePlayerStats = {}

        playerStatsTable.update({k: homePlayerStats})
        k += 1

    for player in homePlayerList:
        if player not in gamePlayerList:
            gamePlayerList.append(player)

    print(gameId)
    
gamesOutput = json.dumps(games, indent = 6,  separators = (", ",":"), sort_keys = True)
gamesOutputJson = 'games.json'
f = open(gamesOutputJson, 'w') #use 'a' to append
f.write(gamesOutput)
f.close()

gameResultsOutput = json.dumps(gameResults, indent = 6,  separators = (", ",":"), sort_keys = True)
gameResultsOutputJson = 'gameResults.json'
f = open(gameResultsOutputJson, 'w') #use 'a' to append
f.write(gameResultsOutput)
f.close()

playerStatsOutput = json.dumps(playerStatsTable, indent = 6,  separators = (", ",":"), sort_keys = True)
playerStatsOutputJson = 'gamePlayerStats.json'
f = open(playerStatsOutputJson, 'w') #use 'a' to append
f.write(playerStatsOutput)
f.close()

with open('gamePlayerList.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
    wr.writerow(gamePlayerList)