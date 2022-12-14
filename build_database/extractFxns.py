## functions

def getGameInfo(gameId, gameData):
    gameTable = {
                'gameId': gameId,
                'season': gameData['gameData']['game']['season'],
                'dateTime': gameData['gameData']['datetime']['dateTime'],
                'homeTeam': gameData['gameData']['teams']['home']['id'],
                'awayTeam' : gameData['gameData']['teams']['away']['id'],
                'status': gameData['gameData']['status']['detailedState']
                }
    return gameTable

def getGameResult(gameId, gameData): 
    gameResultsTable = {
                'gameId': gameId,
                'homeTeamScore': gameData['liveData']['linescore']['teams']['home']['goals'],
                'awayTeamScore': gameData['liveData']['linescore']['teams']['away']['goals'],
                'endType': gameData['liveData']['linescore']['currentPeriod']
                }
    return gameResultsTable

def listSkaters(gameData, side):
    skatersList = list(gameData['liveData']['boxscore']['teams'][side]['skaters']) 
    skatersIdList = []
    for Id in skatersList:
        skatersIdList.append('ID' + str(Id))
    return skatersIdList 

def listGoalies(gameData, side):
    goaliesList = list(gameData['liveData']['boxscore']['teams'][side]['goalies'])
    goaliesIdList = []
    for Id in goaliesList:
        goaliesIdList.append('ID' + str(Id))
    return goaliesIdList

def getSkaterStats(gameId, gameData, side, Id):
    players = gameData['liveData']['boxscore']['teams'][side]['players']
    playerId = players[Id]['person']['id']  
    team = gameData['liveData']['boxscore']['teams'][side]['team']['id']         
    skaterStats = players[Id]['stats']['skaterStats']
        
    if len(skaterStats['timeOnIce']) == 4:
        skaterTimeOnIce = '0' +  skaterStats['timeOnIce']
    else:
        skaterTimeOnIce = skaterStats['timeOnIce']

    if 'powerPlayTimeOnIce' in skaterStats:
        if len(skaterStats['powerPlayTimeOnIce']) == 4:
            timeOnIcePP = '0' +  skaterStats['powerPlayTimeOnIce']
        else:
            timeOnIcePP = skaterStats['powerPlayTimeOnIce']
    else: 
        timeOnIcePP = '00:00'

    if 'shortHandedTimeOnIce' in skaterStats:
        if len(skaterStats['shortHandedTimeOnIce']) == 4:
            timeOnIcePK = '0' +  skaterStats['shortHandedTimeOnIce']
        else:
            timeOnIcePK = skaterStats['shortHandedTimeOnIce']
    else:
        timeOnIcePK = '00:00'

    if 'hits' in skaterStats:
        hits = skaterStats['hits']
    else:
        hits = 9999
    
    if 'blocked' in skaterStats:
        blocks = skaterStats['blocked']
    else:
        blocks = 9999

    if 'faceoffTaken' in skaterStats:
        faceoffsTaken = skaterStats['faceoffTaken']
    else:
        faceoffsTaken = 9999

    if 'faceOffWins' in skaterStats:
        faceoffsWon = skaterStats['faceOffWins']
    else:
        faceoffsWon = 9999    

    if 'takeaways' in skaterStats:
        takeaways = skaterStats['takeaways']
    else:
        takeaways = 9999  

    if 'giveaways' in skaterStats:
        giveaways = skaterStats['giveaways']
    else:
        giveaways = 9999  

    skaterStats = {
                    'gameId': gameId,
                    'playerId': playerId,
                    'team': team,
                    'goals': skaterStats['goals'],
                    'goalsPP': skaterStats['powerPlayGoals'],
                    'goalsPK': skaterStats['shortHandedGoals'],
                    'assists': skaterStats['assists'],
                    'assistsPP': skaterStats['powerPlayAssists'],
                    'assistsPK': skaterStats['shortHandedAssists'],
                    'shotsOnGoal': skaterStats['shots'],
                    'penaltyMin': skaterStats['penaltyMinutes'],
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

    return skaterStats

def getGoalieStats(gameId, gameData, side, Id):
    players = gameData['liveData']['boxscore']['teams'][side]['players']
    playerId = players[Id]['person']['id']
    team = gameData['liveData']['boxscore']['teams']['home']['team']['id']
    goalieStats = players[Id]['stats']['goalieStats']

    if len(goalieStats['timeOnIce']) == 4:
        goalieTimeOnIce = '00:0' +  goalieStats['timeOnIce']
    elif len(goalieStats['timeOnIce']) == 5:
        goalieTimeOnIce = '00:' +  goalieStats['timeOnIce']
    else:
        goalieTimeOnIce = goalieStats['timeOnIce']

    if goalieTimeOnIce[:4] == '00:6':
        goalieTimeOnIce = '01:0' + goalieTimeOnIce[4] + goalieTimeOnIce[5:]

    if 'powerPlayShotsAgainst' in goalieStats:
        shotsFacedPP = goalieStats['powerPlayShotsAgainst']
    else:
        shotsFacedPP = 9999  

    if 'shortHandedShotsAgainst' in goalieStats:
        shotsFacedPK = goalieStats['shortHandedShotsAgainst']
    else:
        shotsFacedPK = 9999 

    if 'powerPlaySaves' in goalieStats:
        savesPP = goalieStats['powerPlaySaves']
    else:
        savesPP = 9999 

    if 'shortHandedSaves' in goalieStats:
        savesPK = goalieStats['shortHandedSaves']
    else:
        savesPK = 9999 

    goalieStats = {
                    'gameId': gameId,
                    'playerId': playerId,
                    'team': team,
                    'goals': goalieStats['goals'],
                    'assists': goalieStats['assists'],
                    'penaltyMin': goalieStats['pim'],
                    'shotsFaced': goalieStats['shots'],
                    'shotsFacedPP': shotsFacedPP,
                    'shotsFacedPK': shotsFacedPK,
                    'saves': goalieStats['saves'],
                    'savesPP': savesPP,
                    'savesPK': savesPK,
                    'timeOnIce': goalieTimeOnIce,
                    'decision': goalieStats['decision']
                    }
    return goalieStats