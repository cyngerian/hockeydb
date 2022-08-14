import psycopg2
import json
from config import config


def divisionsLoad():
    f = open('divisions.json')
    divData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in divData:
            divs = divData[row]        
            cur.execute("INSERT INTO nhldb.divisions(divisionid, name, conferenceid, abbreviation, active) VALUES (%s, %s, %s, %s, %s)", (divs['id'], divs['name'], divs['conferenceId'], divs['abbreviation'], divs['active']))
            
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
    divisionsLoad()




