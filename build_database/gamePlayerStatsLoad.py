import psycopg2
import json
from config import config


def gamePlayerStatsLoad():
    f = open('gamePlayerStats.json')
    gamePlayerStatsData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in gamePlayerStatsData:
            gamePlayerStats = gamePlayerStatsData[row]        
            cur.execute("INSERT INTO nhldb.gamePlayerStats(gameid, playerid, goals, assists, hits, shotsongoal, penaltyminutes, blocks, timeonice, timeonicepowerplay, timeonicepenaltykill, faceoffstaken, faceoffswon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (gamePlayerStats['gameId'], gamePlayerStats['playerId'], gamePlayerStats['goals'], gamePlayerStats['assists'], gamePlayerStats['hits'], gamePlayerStats['shotsOnGoal'], gamePlayerStats['penaltyMin'], gamePlayerStats['blocks'], gamePlayerStats['timeOnIce'], gamePlayerStats['powerPlayTOI'], gamePlayerStats['penaltyKillTOI'], gamePlayerStats['faceoffsTaken'], gamePlayerStats['faceoffsWon']))
            
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    gamePlayerStatsLoad()




