import psycopg2
import json
from config import config

sql = """
        INSERT INTO nhldb.gameGoalieStats (
            gameid,
            playerid,
            teamid,
            goals,
            assists,
            penaltymin,
            shotsfaced,
            shotsfacedpp,
            shotsfacedpk,
            saves,
            savespp,
            savespk,
            timeonice,
            decision)
        VALUES (%s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s)
      """

def gameGoalieStatsLoad():
    f = open('gameGoalieStats.json')
    gameGoalieStatsData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one 
        for row in gameGoalieStatsData:
            goalies = gameGoalieStatsData[row]  
            cur.execute(sql, (goalies['gameId'], 
                                goalies['playerId'], 
                                goalies['team'],
                                goalies['goals'],
                                goalies['assists'], 
                                goalies['penaltyMin'], 
                                goalies['shotsFaced'], 
                                goalies['shotsFacedPP'],
                                goalies['shotsFacedPK'],
                                goalies['saves'],
                                goalies['savesPP'],
                                goalies['savesPK'],
                                goalies['timeOnIce'],
                                goalies['decision']))

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
    gameGoalieStatsLoad()