import psycopg2
import json
from config import config

sql = """
        INSERT INTO nhldb.seasons (
            seasonid, 
            seasonstartregular, 
            seasonendregular, 
            seasonstartpost, 
            seasonendpost, 
            numberofgames, 
            tiesinuse)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
      """

def seasonsLoad():
    f = open('seasons.json')
    seasonData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in seasonData:
            seasons = seasonData[row]        
            cur.execute(sql, (seasons['seasonId'], 
                              seasons['seasonStartRegular'], 
                              seasons['seasonEndRegular'], 
                              seasons['seasonStartPost'], 
                              seasons['seasonEndPost'], 
                              seasons['numberOfGames'], 
                              seasons['tiesInUse']))
            
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
    seasonsLoad()




