import psycopg2
import json
from config import config


def teamsLoad():
    f = open('teams.json')
    teamData = json.load(f)
    row = 0

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for row in teamData:
            teams = teamData[row]        
            cur.execute("INSERT INTO nhldb.teams(teamid, name, abbreviation, divisionid, venue, city, location ) VALUES (%s, %s, %s, %s, %s, %s, %s)", (teams['teamId'], teams['name'], teams['abbreviation'], teams['divisionId'], teams['venue'], teams['city'], teams['location']))
            
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
    teamsLoad()




