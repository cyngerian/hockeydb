import psycopg2
import json
from config import config

sql = """
        INSERT INTO nhldb.gameSkaterStats (
            gameid,
            playerid,
            teamid,
            goals,
            goalspp,
            goalspk,
            assists,
            assistspp,
            assistspk,
            hits,
            shotsongoal,
            penaltymin,
            blocks,
            timeonice,
            timeonicepp,
            timeonicepk,
            faceoffstaken,
            faceoffswon,
            takeaways,
            giveaways)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
      """

def gameSkaterStatsLoad():
    f = open('gameSkaterStats.json')
    gameSkaterStatsData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one 
        for row in gameSkaterStatsData:
            skaters = gameSkaterStatsData[row]  
            cur.execute(sql, (skaters ['gameId'], 
                                skaters['playerId'], 
                                skaters['team'],
                                skaters['goals'],
                                skaters['goalsPP'], 
                                skaters['goalsPK'], 
                                skaters['assists'], 
                                skaters['assistsPP'], 
                                skaters['assistsPK'], 
                                skaters['hits'], 
                                skaters['shotsOnGoal'], 
                                skaters['penaltyMin'], 
                                skaters['blocks'],
                                skaters['timeOnIce'],
                                skaters['timeOnIcePP'], 
                                skaters['timeOnIcePK'], 
                                skaters['faceoffsTaken'], 
                                skaters['faceoffsWon'], 
                                skaters['takeaways'], 
                                skaters['giveaways']))

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
    gameSkaterStatsLoad()