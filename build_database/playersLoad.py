import psycopg2
import json
from config import config

sql = """
        INSERT INTO nhldb.players (
            playerid,
            namefirst,
            namelast,
            primarynumber,
            birthdate,
            birthcity,
            birthcountry,
            nationality,
            height,
            weight,
            shootscatches,
            primaryposition,
            active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
      """

def playersLoad():
    f = open('players.json')
    playersData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in playersData:
            players = playersData[row]  
            print(players['playerId'])   
            cur.execute(sql, (players['playerId'], 
                                players['nameFirst'], 
                                players['nameLast'],
                                players['primaryNumber'],
                                players['birthDate'], 
                                players['birthCity'], 
                                players['birthCountry'], 
                                players['nationality'], 
                                players['height'], 
                                players['weight'], 
                                players['shootsCatches'],
                                players['primaryPosition'],    
                                players['active']))

            
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




