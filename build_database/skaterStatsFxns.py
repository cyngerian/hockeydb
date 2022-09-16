import requests
import json
import time


def listPLayers(gameData, side):
    players = gameData['liveData']['boxscore']['teams'][side]['players']
    playerList = []
    playerIdList = list(players)

    for Id in playerIdList:
        playerId = players[Id]['person']['id']
        playerList.append(playerId)

    return playerList, playerIdList

def skaterStatsDict(gameData, side, Id):
    players = gameData['liveData']['boxscore']['teams'][side]['players']
    gameId = gameData['gamePk']
    playerId = players[Id]['person']['id']

    if 'skaterStats' in players[Id]['stats']:                    
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
                        'team': gameData['liveData']['boxscore']['teams'][side]['team']['id'],
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

def goalieStatsDict(gameData, side, Id):
    players = gameData['liveData']['boxscore']['teams'][side]['players']
    gameId = gameData['gamePk']
    playerId = players[Id]['person']['id']


if __name__ == '__main__':
    skaterStatsDict()