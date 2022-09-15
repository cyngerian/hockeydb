import requests
import json
import pandas as pd
import time

startUrl = 'https://statsapi.web.nhl.com/api/v1/game/'
endUrl = '/feed/live'
startYear = 1967
startGame = 20001
url = startUrl + str(startYear) + '0' + str(startGame) + endUrl

n = 0
runStartTime = time.time()

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
t = 0.25
while startYear < 2022:
    response = requests.get(url)
    gameJson = response.json()
    data = json.dumps(gameJson)
    gameData = json.loads(data)

    time.sleep(t)

    if 'gamePk' in gameData:
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

                if 'powerPlayTimeOnIce' in awaySkaterStats:
                    if len(awaySkaterStats['powerPlayTimeOnIce']) == 4:
                        timeOnIcePP = '0' +  awaySkaterStats['powerPlayTimeOnIce']
                    else:
                        timeOnIcePP = awaySkaterStats['powerPlayTimeOnIce']
                else: 
                    timeOnIcePP = '00:00'

                if 'shortHandedTimeOnIce' in awaySkaterStats:
                    if len(awaySkaterStats['shortHandedTimeOnIce']) == 4:
                        timeOnIcePK = '0' +  awaySkaterStats['shortHandedTimeOnIce']
                    else:
                        timeOnIcePK = awaySkaterStats['shortHandedTimeOnIce']
                else:
                    timeOnIcePK = '00:00'

                if 'hits' in awayPlayerStats:
                    hits = awaySkaterStats['hits']
                else:
                    hits = 9999
                
                if 'blocked' in awayPlayerStats:
                    blocks = awaySkaterStats['blocked']
                else:
                    blocks = 9999

                if 'faceoffTaken' in awayPlayerStats:
                    faceoffsTaken = awaySkaterStats['faceoffTaken']
                else:
                    faceoffsTaken = 9999

                if 'faceOffWins' in awayPlayerStats:
                    faceoffsWon = awaySkaterStats['faceOffWins']
                else:
                    faceoffsWon = 9999    

                if 'takeaways' in awayPlayerStats:
                    takeaways = awaySkaterStats['takeaways']
                else:
                    takeaways = 9999  

                if 'giveaways' in awayPlayerStats:
                    giveaways = awaySkaterStats['giveaways']
                else:
                    giveaways = 9999  
                
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
                                'shotsOnGoal': awaySkaterStats['shots'],
                                'penaltyMin': awaySkaterStats['penaltyMinutes'],
                                'timeOnIce': '00:' + skaterTimeOnIce,

                                'hits': hits,
                                'blocks': blocks,
                                'timeOnIcePP': '00:' + timeOnIcePP,
                                'timeOnIcePK': '00:' + timeOnIcePK,
                                'faceoffsTaken': faceoffsTaken,
                                'faceoffsWon': faceoffsWon,
                                'takeaways': takeaways,
                                'giveaways': giveaways
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

                if 'powerPlayShotsAgainst' in awayGoalieStats:
                    shotsFacedPP = awayGoalieStats['powerPlayShotsAgainst']
                else:
                    shotsFacedPP = 9999  

                if 'shortHandedShotsAgainst' in awayGoalieStats:
                    shotsFacedPK = awayGoalieStats['shortHandedShotsAgainst']
                else:
                    shotsFacedPK = 9999 

                if 'powerPlaySaves' in awayGoalieStats:
                    savesPP = awayGoalieStats['powerPlaySaves']
                else:
                    savesPP = 9999 

                if 'shortHandedSaves' in awayGoalieStats:
                    savesPK = awayGoalieStats['shortHandedSaves']
                else:
                    savesPK = 9999 

                awayGoalieStats = {
                                'gameId': gameId,
                                'playerId': awayPlayerId,
                                'team': gameData['liveData']['boxscore']['teams']['away']['team']['id'],
                                'goals': awayGoalieStats['goals'],
                                'assists': awayGoalieStats['assists'],
                                'penaltyMin': awayGoalieStats['pim'],
                                'shotsFaced': awayGoalieStats['shots'],
                                'shotsFacedPP': shotsFacedPP,
                                'shotsFacedPK': shotsFacedPK,
                                'saves': awayGoalieStats['saves'],
                                'savesPP': savesPP,
                                'savesPK': savesPK,
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

                if len(homeSkaterStats['timeOnIce']) == 4:
                    skaterTimeOnIce = '0' +  homeSkaterStats['timeOnIce']
                else:
                    skaterTimeOnIce = homeSkaterStats['timeOnIce']

                if 'powerPlayTimeOnIce' in homeSkaterStats:
                    if len(homeSkaterStats['powerPlayTimeOnIce']) == 4:
                        timeOnIcePP = '0' +  homeSkaterStats['powerPlayTimeOnIce']
                    else:
                        timeOnIcePP = homeSkaterStats['powerPlayTimeOnIce']
                else: 
                    timeOnIcePP = '00:00'

                if 'shortHandedTimeOnIce' in homeSkaterStats:
                    if len(homeSkaterStats['shortHandedTimeOnIce']) == 4:
                        timeOnIcePK = '0' +  homeSkaterStats['shortHandedTimeOnIce']
                    else:
                        timeOnIcePK = homeSkaterStats['shortHandedTimeOnIce']
                else:
                    timeOnIcePK = '00:00'

                if 'hits' in homePlayerStats:
                    hits = homeSkaterStats['hits']
                else:
                    hits = 9999
                
                if 'blocked' in homePlayerStats:
                    blocks = homeSkaterStats['blocked']
                else:
                    blocks = 9999

                if 'faceoffTaken' in homePlayerStats:
                    faceoffsTaken = homeSkaterStats['faceoffTaken']
                else:
                    faceoffsTaken = 9999

                if 'faceOffWins' in homePlayerStats:
                    faceoffsWon = homeSkaterStats['faceOffWins']
                else:
                    faceoffsWon = 9999    

                if 'takehomes' in homePlayerStats:
                    takehomes = homeSkaterStats['takehomes']
                else:
                    takehomes = 9999  

                if 'givehomes' in homePlayerStats:
                    givehomes = homeSkaterStats['givehomes']
                else:
                    givehomes = 9999  
                
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
                                'shotsOnGoal': homeSkaterStats['shots'],
                                'penaltyMin': homeSkaterStats['penaltyMinutes'],
                                'timeOnIce': '00:' + skaterTimeOnIce,

                                'hits': hits,
                                'blocks': blocks,
                                'timeOnIcePP': '00:' + timeOnIcePP,
                                'timeOnIcePK': '00:' + timeOnIcePK,
                                'faceoffsTaken': faceoffsTaken,
                                'faceoffsWon': faceoffsWon,
                                'takehomes': takehomes,
                                'givehomes': givehomes
                                }

            elif 'goalieStats' in homePlayers[Id]['stats']:
                homeGoalieStats = homePlayers[Id]['stats']['goalieStats']

                if len(homeGoalieStats['timeOnIce']) == 4:
                    goalieTimeOnIce = '00:0' +  homeGoalieStats['timeOnIce']
                elif len(homeGoalieStats['timeOnIce']) == 5:
                    goalieTimeOnIce = '00:' +  homeGoalieStats['timeOnIce']
                else:
                    goalieTimeOnIce = homeGoalieStats['timeOnIce']

                if goalieTimeOnIce[:4] == '00:6':
                    goalieTimeOnIce = '01:0' + goalieTimeOnIce[4] + goalieTimeOnIce[5:]

                if 'powerPlayShotsAgainst' in homeGoalieStats:
                    shotsFacedPP = homeGoalieStats['powerPlayShotsAgainst']
                else:
                    shotsFacedPP = 9999  

                if 'shortHandedShotsAgainst' in homeGoalieStats:
                    shotsFacedPK = homeGoalieStats['shortHandedShotsAgainst']
                else:
                    shotsFacedPK = 9999 

                if 'powerPlaySaves' in homeGoalieStats:
                    savesPP = homeGoalieStats['powerPlaySaves']
                else:
                    savesPP = 9999 

                if 'shortHandedSaves' in homeGoalieStats:
                    savesPK = homeGoalieStats['shortHandedSaves']
                else:
                    savesPK = 9999 

                homeGoalieStats = {
                                'gameId': gameId,
                                'playerId': homePlayerId,
                                'team': gameData['liveData']['boxscore']['teams']['home']['team']['id'],
                                'goals': homeGoalieStats['goals'],
                                'assists': homeGoalieStats['assists'],
                                'penaltyMin': homeGoalieStats['pim'],
                                'shotsFaced': homeGoalieStats['shots'],
                                'shotsFacedPP': shotsFacedPP,
                                'shotsFacedPK': shotsFacedPK,
                                'saves': homeGoalieStats['saves'],
                                'savesPP': savesPP,
                                'savesPK': savesPK,
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

        n += 1 
        currentTime = time.time()
        elapsedTime = "%.2f" % (currentTime - runStartTime) 
        elapsed = float(currentTime - runStartTime)
        totalGames = 55166
        gamesLeft = totalGames - n
        gamesPerSecond = n / elapsed
        if gamesPerSecond < 4:
            t = t - 0.001
            if t == 0.001:
                t = t + 0.001
        else: 
            t = t + 0.001
        hoursLeft = (gamesLeft / gamesPerSecond) / 3600
        print(str(n) + '  ' + str(gameId)[:4] + ' ' + str(gameId)[-4:] 
              + '   ' + elapsedTime + ' sec  ' + str(gamesPerSecond)[:5] 
              + ' games/sec  ' + str(hoursLeft)[:5] + ' hrs left  ' 
              + str(100 * (n / totalGames))[:5] + '% ' + ' t = ' + str(t)[:5])

        startGame += 1
        url = startUrl + str(startYear) + '0' + str(startGame) + endUrl

    else: 
        startGame = 20001
        startYear += 1
        if startYear == 2004:
            startYear += 1
        url = startUrl + str(startYear) + '0' + str(startGame) + endUrl
    



gamesOutput = json.dumps(games, indent = 6,  separators = (", ",":"), sort_keys = True)
gamesOutputJson = 'gamesAll_nl.json'
f = open(gamesOutputJson, 'w') #use 'a' to append
f.write(gamesOutput)
f.close()

gameResultsOutput = json.dumps(gameResults, indent = 6,  separators = (", ",":"), sort_keys = True)
gameResultsOutputJson = 'gameResultsAll_nl.json'
f = open(gameResultsOutputJson, 'w') #use 'a' to append
f.write(gameResultsOutput)
f.close()

skaterStatsOutput = json.dumps(skaterStatsTable, indent = 6,  separators = (", ",":"), sort_keys = True)
skaterStatsOutputJson = 'gameSkaterStatsAll_nl.json'
f = open(skaterStatsOutputJson, 'w') #use 'a' to append
f.write(skaterStatsOutput)
f.close()

goalieStatsOutput = json.dumps(goalieStatsTable, indent = 6,  separators = (", ",":"), sort_keys = True)
goalieStatsOutputJson = 'gameGoalieStatsAll_nl.json'
f = open(goalieStatsOutputJson, 'w') #use 'a' to append
f.write(goalieStatsOutput)
f.close()

df = pd.DataFrame(data={"players": gamePlayerList})

df.to_csv("./gamePlayerListAll_nl.csv", sep=',',index=False)