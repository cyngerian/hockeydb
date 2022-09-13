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
skaterStatsTable = {}
goalieStatsTable = {}

i = 0
j = 0
s = 0
g = 0
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

            if len(awaySkaterStats['timeOnIce']) == 4:
                skaterTimeOnIce = '0' +  awaySkaterStats['timeOnIce']
            else:
                skaterTimeOnIce = awaySkaterStats['timeOnIce']

            if len(awaySkaterStats['powerPlayTimeOnIce']) == 4:
                timeOnIcePP = '0' +  awaySkaterStats['powerPlayTimeOnIce']
            else:
                timeOnIcePP = awaySkaterStats['powerPlayTimeOnIce']

            if len(awaySkaterStats['shortHandedTimeOnIce']) == 4:
                timeOnIcePK = '0' +  awaySkaterStats['shortHandedTimeOnIce']
            else:
                timeOnIcePK = awaySkaterStats['shortHandedTimeOnIce']

            awaySkaterStats = {
                            'gameId': gameId,
                            'playerId': awayPlayerId,
                            'team': gameData['liveData']['boxscore']['teams']['away']['team']['id'],
                            'goals': awaySkaterStats['goals'],
                            'goalsPP': awaySkaterStats['powerPlayGoals'],
                            'goalsPK': awaySkaterStats['shortHandedGoals'],
                            'assists': awaySkaterStats['assists'],
                            'assistsPP': awaySkaterStats['powerPlayAssists'],
                            'assistsPK': awaySkaterStats['shortHandedAssists'],
                            'hits': awaySkaterStats['hits'],
                            'shotsOnGoal': awaySkaterStats['shots'],
                            'penaltyMin': awaySkaterStats['penaltyMinutes'],
                            'blocks': awaySkaterStats['blocked'],
                            'timeOnIce': '00:' + skaterTimeOnIce,
                            'timeOnIcePP': '00:' + timeOnIcePP,
                            'timeOnIcePK': '00:' + timeOnIcePK,
                            'faceoffsTaken': awaySkaterStats['faceoffTaken'],
                            'faceoffsWon': awaySkaterStats['faceOffWins'],
                            'takeaways': awaySkaterStats['takeaways'],
                            'giveaways': awaySkaterStats['giveaways']
                            }

        elif 'goalieStats' in awayPlayers[Id]['stats']:
            awayGoalieStats = awayPlayers[Id]['stats']['goalieStats']

            if len(awayGoalieStats['timeOnIce']) == 4:
                goalieTimeOnIce = '00:0' +  awayGoalieStats['timeOnIce']
            elif len(awayGoalieStats['timeOnIce']) == 5:
                goalieTimeOnIce = '00:' +  awayGoalieStats['timeOnIce']
            else:
                goalieTimeOnIce = awayGoalieStats['timeOnIce']

            if goalieTimeOnIce[:4] == '00:6':
                goalieTimeOnIce = '01:0' + goalieTimeOnIce[4] + goalieTimeOnIce[5:]

            awayGoalieStats = {
                            'gameId': gameId,
                            'playerId': awayPlayerId,
                            'team': gameData['liveData']['boxscore']['teams']['away']['team']['id'],
                            'goals': awayGoalieStats['goals'],
                            'assists': awayGoalieStats['assists'],
                            'penaltyMin': awayGoalieStats['pim'],
                            'shotsFaced': awayGoalieStats['shots'],
                            'shotsFacedPP': awayGoalieStats['powerPlayShotsAgainst'],
                            'shotsFacedPK': awayGoalieStats['shortHandedShotsAgainst'],
                            'saves': awayGoalieStats['saves'],
                            'savesPP': awayGoalieStats['powerPlaySaves'],
                            'savesPK': awayGoalieStats['shortHandedSaves'],
                            'timeOnIce': goalieTimeOnIce,
                            'decision': awayGoalieStats['decision']
                            }


        else: awayPlayerStats = {}

        if 'skaterStats' in awayPlayers[Id]['stats']:
            skaterStatsTable.update({s: awaySkaterStats})
            s += 1

        if 'goalieStats' in awayPlayers[Id]['stats']:
            goalieStatsTable.update({g: awayGoalieStats})
            g += 1

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

            if 'skaterStats' in homePlayers[Id]['stats']:
                homeSkaterStats = homePlayers[Id]['stats']['skaterStats']
                
                if len(homeSkaterStats['timeOnIce']) == 4:
                    timeOnIce = '0' +  homeSkaterStats['timeOnIce']
                else:
                    timeOnIce = homeSkaterStats['timeOnIce']

                if len(homeSkaterStats['powerPlayTimeOnIce']) == 4:
                    timeOnIcePP = '0' +  homeSkaterStats['powerPlayTimeOnIce']
                else:
                    timeOnIcePP = homeSkaterStats['powerPlayTimeOnIce']

                if len(homeSkaterStats['shortHandedTimeOnIce']) == 4:
                    timeOnIcePK = '0' +  homeSkaterStats['shortHandedTimeOnIce']
                else:
                    timeOnIcePK = homeSkaterStats['shortHandedTimeOnIce']
            
            homeSkaterStats = {
                            'gameId': gameId,
                            'playerId': homePlayerId,
                            'team': gameData['liveData']['boxscore']['teams']['home']['team']['id'],
                            'goals': homeSkaterStats['goals'],
                            'goalsPP': homeSkaterStats['powerPlayGoals'],
                            'goalsPK': homeSkaterStats['shortHandedGoals'],
                            'assists': homeSkaterStats['assists'],
                            'assistsPP': homeSkaterStats['powerPlayAssists'],
                            'assistsPK': homeSkaterStats['shortHandedAssists'],
                            'hits': homeSkaterStats['hits'],
                            'shotsOnGoal': homeSkaterStats['shots'],
                            'penaltyMin': homeSkaterStats['penaltyMinutes'],
                            'blocks': homeSkaterStats['blocked'],
                            'timeOnIce': '00:' + timeOnIce,
                            'timeOnIcePP': '00:' + timeOnIcePP,
                            'timeOnIcePK': '00:' + timeOnIcePK,
                            'faceoffsTaken': homeSkaterStats['faceoffTaken'],
                            'faceoffsWon': homeSkaterStats['faceOffWins'],
                            'takeaways': homeSkaterStats['takeaways'],
                            'giveaways': homeSkaterStats['giveaways']
                            }

        elif 'goalieStats' in homePlayers[Id]['stats']:
            homeGoalieStats = homePlayers[Id]['stats']['goalieStats']

            if len(homeGoalieStats['timeOnIce']) == 4:
                goalieTimeOnIce = '00:0' +  homeGoalieStats['timeOnIce']
            elif len(homeGoalieStats['timeOnIce']) == 5:
                goalieTimeOnIce = '00:' +  homeGoalieStats['timeOnIce']
            else:
                goalieTimeOnIce = homeGoalieStats['timeOnIce']

            if str(goalieTimeOnIce[:4]) == '00:6':
                goalieTimeOnIce = '01:0' + goalieTimeOnIce[4] + goalieTimeOnIce[5:]

            homeGoalieStats = {
                            'gameId': gameId,
                            'playerId': homePlayerId,
                            'team': gameData['liveData']['boxscore']['teams']['home']['team']['id'],
                            'goals': homeGoalieStats['goals'],
                            'assists': homeGoalieStats['assists'],
                            'penaltyMin': homeGoalieStats['pim'],
                            'shotsFaced': homeGoalieStats['shots'],
                            'shotsFacedPP': homeGoalieStats['powerPlayShotsAgainst'],
                            'shotsFacedPK': homeGoalieStats['shortHandedShotsAgainst'],
                            'saves': homeGoalieStats['saves'],
                            'savesPP': homeGoalieStats['powerPlaySaves'],
                            'savesPK': homeGoalieStats['shortHandedSaves'],
                            'timeOnIce': goalieTimeOnIce,
                            'decision': homeGoalieStats['decision']
                            }

        else: homePlayerStats = {}

        if 'skaterStats' in homePlayers[Id]['stats']:
            skaterStatsTable.update({s: homeSkaterStats})
            s += 1

        if 'goalieStats' in homePlayers[Id]['stats']:
            goalieStatsTable.update({g: homeGoalieStats})
            g += 1


    for player in homePlayerList:
        if player not in gamePlayerList:
            gamePlayerList.append(player)

    print(gameId)
    
gamesOutput = json.dumps(games, indent = 6,  separators = (", ",":"), sort_keys = True)
gamesOutputJson = 'gamesAll.json'
f = open(gamesOutputJson, 'w') #use 'a' to append
f.write(gamesOutput)
f.close()

gameResultsOutput = json.dumps(gameResults, indent = 6,  separators = (", ",":"), sort_keys = True)
gameResultsOutputJson = 'gameResultsAll.json'
f = open(gameResultsOutputJson, 'w') #use 'a' to append
f.write(gameResultsOutput)
f.close()

skaterStatsOutput = json.dumps(skaterStatsTable, indent = 6,  separators = (", ",":"), sort_keys = True)
skaterStatsOutputJson = 'gameSkaterStatsAll.json'
f = open(skaterStatsOutputJson, 'w') #use 'a' to append
f.write(skaterStatsOutput)
f.close()

goalieStatsOutput = json.dumps(goalieStatsTable, indent = 6,  separators = (", ",":"), sort_keys = True)
goalieStatsOutputJson = 'gameGoalieStatsAll.json'
f = open(goalieStatsOutputJson, 'w') #use 'a' to append
f.write(goalieStatsOutput)
f.close()

with open('gamePlayerListAll.csv', 'w+', newline='') as myfile:
    wr = csv.writer(myfile, delimiter=',', quoting=csv.QUOTE_NONE)
    wr.writerow(gamePlayerList)