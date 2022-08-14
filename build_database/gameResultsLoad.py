import psycopg2
import json
from config import config


def gameResultsLoad():
    f = open('gameResults.json')
    gameResultsData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in gameResultsData:
            gameResults = gameResultsData[row]        
            cur.execute("INSERT INTO nhldb.gameresults(gameid, hometeamscore, awayteamscore, endtype) VALUES (%s, %s, %s, %s)", (gameResults['gameId'], gameResults['homeTeamScore'], gameResults['awayTeamScore'], gameResults['endType']))
            
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
    gameResultsLoad()




