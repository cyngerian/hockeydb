import psycopg2
import json
from config import config


def playersLoad():
    f = open('playerInfo.json')
    playerData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in playerData:
            players = playerData[row]        
            cur.execute("INSERT INTO nhldb.players(playerid, namelast, namefirst, primarynumber, birthdate, birthcity, birthcountry, nationality, height, weight, shootscatches, primaryposition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (players['playerId'], players['lastName'], players['firstName'], players['primaryNumber'], players['birthDate'], players['birthCity'], players['birthCountry'], players['nationality'], players['height'], players['weight'], players['shootsCatches'], players['primaryPosition']))
            
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
    playersLoad()




