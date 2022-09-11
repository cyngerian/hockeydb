import psycopg2
import json
from config import config

sql = """
        INSERT INTO nhldb.games (
            gameid,
            seasonid,
            hometeamid,
            awayteamid,
            datetime,
            status) 
        VALUES (%s, %s, %s, %s, %s, %s)
      """

def gamesLoad():
    f = open('games.json')
    gameData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in gameData:
            games = gameData[row]        
            cur.execute(sql, (games['gameId'],
                              games['season'],
                              games['homeTeam'], 
                              games['awayTeam'], 
                              games['dateTime'], 
                              games['status']))
            
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
    gamesLoad()




