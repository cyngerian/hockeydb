import psycopg2
import json
from config import config

sql = """
        INSERT INTO nhldb.conferences(
            conferenceid,
            name,
            abbreviation,
            shortname,
            active)
        VALUES (%s, %s, %s, %s, %s)
      """

def conferencesLoad():
    f = open('conferences.json')
    confData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in confData:
            confs = confData[row]        
            cur.execute(sql, (confs['id'], 
                              confs['name'], 
                              confs['abbreviation'], 
                              confs['shortName'], 
                              confs['active']))
            
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
    conferencesLoad()




