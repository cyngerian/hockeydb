import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS nhldb.teamstest (
            teamID integer NOT NULL,
            name character varying(50) NOT NULL,
            abbreviation character varying(5) NOT NULL,
            city character varying(50) NOT NULL,
            divisionID integer NOT NULL,
            venue character varying(25) NOT NULL,
            location character varying(25) NOT NULL,
            PRIMARY KEY (teamID)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
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
    create_tables()