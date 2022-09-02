import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS nhldb.teams (
            teamID integer NOT NULL,
            name character varying(50) NOT NULL,
            abbreviation character varying(5) NOT NULL,
            city character varying(50) NOT NULL,
            divisionID integer NOT NULL,
            venue character varying(25) NOT NULL,
            location character varying(25) NOT NULL,
            PRIMARY KEY (teamID)
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS nhldb.divisions 
        (
            divisionID integer NOT NULL,
            name character varying(15) NOT NULL,
            conferenceID integer NOT NULL,
            abbreviation character varying(1) NOT NULL,
            active boolean NOT NULL,
            PRIMARY KEY (divisionID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS nhldb.conferences 
        (
            conferenceID integer NOT NULL,
            name character varying(10) NOT NULL,
            abbreviation character varying(1) NOT NULL,
            shortName character varying(10) NOT NULL,
            active boolean NOT NULL,
            PRIMARY KEY (conferenceID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS nhldb.players 
        (
            playerID integer NOT NULL,
            nameLast character varying(35) NOT NULL,
            nameFirst character varying(35) NOT NULL,
            primaryNumber integer NULL,
            birthDate date NOT NULL,
            birthCity character varying(25) NOT NULL,
            birthCountry character varying(5) NOT NULL,
            nationality character varying(5) NOT NULL,
            height character varying(10) NOT NULL,
            weight integer NOT NULL,
            shootsCatches character varying(1) NOT NULL,
            primaryPosition character varying(3) NOT NULL,
            PRIMARY KEY (playerID)
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS nhldb.seasons
        (
            seasonID integer NOT NULL,
            seasonStartRegular date NOT NULL,
            seasonEndRegular date NOT NULL,
            seasonStartPost date NOT NULL,
            seasonEndPost date NOT NULL,
            numberOfGames integer NOT NULL,
            tiesInUse boolean NOT NULL,
            PRIMARY KEY (seasonID)
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS nhldb.games
        ( 
            gameID integer NOT NULL,
            seasonID integer NOT NULL,
            homeTeamID integer NOT NULL,
            awayTeamID integer NOT NULL,
            datetime timestamp with time zone NOT NULL,
            status character varying(15) NOT NULL,
            PRIMARY KEY (gameID)   
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS nhldb.teamsPlayers
        ( 
            playerID integer NOT NULL,
            teamID integer NOT NULL,
            seasonID integer NOT NULL,
            firstGameID integer NOT NULL,
            lastGameID integer NOT NULL,
            active boolean NOT NULL,
            stintNumber integer NOT NULL,
            PRIMARY KEY (playerID, teamID, seasonID, stintNumber)
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS nhldb.gameSkaterStats
        (
            gameID integer NOT NULL,
            playerID integer NOT NULL,
            teamID integer NOT NULL,
            goals integer NOT NULL,
            goalsPP integer NOT NULL,
            goalsPK integer NOT NULL,
            assists integer NOT NULL,
            assistsPP integer NOT NULL,
            assistsPK integer NOT NULL,
            hits integer NOT NULL,
            shotsOnGoal integer NOT NULL,
            penaltyMin integer NOT NULL,
            blocks integer NOT NULL,
            timeOnIce time without time zone NOT NULL,
            timeOnIcePP time without time zone NOT NULL,
            timeOnIcePK time without time zone NOT NULL,
            faceoffsTaken integer NOT NULL,
            faceoffsWon integer NOT NULL,
            takeaways integer NOT NULL,
            giveaways integer NOT NULL,
            PRIMARY KEY (gameID, playerID)    
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS nhldb.gameGoalieStats
        (
            gameID integer NOT NULL,
            playerID integer NOT NULL,
            teamID integer NOT NULL,
            goals integer NOT NULL,
            assists integer NOT NULL,
            penaltyMin integer NOT NULL,
            shotsFaced integer NOT NULL,
            shotsFacedPP integer NOT NULL,
            shotsFacedPK integer NOT NULL,
            saves integer NOT NULL,
            savesPP integer NOT NULL,
            savesPK integer NOT NULL,
            timeOnIce time without time zone NOT NULL,
            decision character varying(1) NOT NULL,
            PRIMARY KEY (gameID, playerID)    
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS nhldb.gameResults
        ( 
            gameID integer NOT NULL,
            homeTeamScore integer NOT NULL,
            awayTeamScore integer NOT NULL,
            endType integer NOT NULL,
            PRIMARY KEY (gameID)
        )
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.teams
            ADD FOREIGN KEY (divisionID)
            REFERENCES nhldb.divisions (divisionID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.divisions
            ADD FOREIGN KEY (conferenceID)
            REFERENCES nhldb.conferences (conferenceID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
#        """ 
#        ALTER TABLE IF EXISTS nhldb.games
#            ADD FOREIGN KEY (seasonID)
#            REFERENCES nhldb.seasons (seasonID) MATCH SIMPLE
#            ON UPDATE NO ACTION
#            ON DELETE NO ACTION
#            NOT VALID
#        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.games
            ADD FOREIGN KEY (homeTeamID)
            REFERENCES nhldb.teams (teamID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.games
            ADD FOREIGN KEY (awayTeamID)
            REFERENCES nhldb.teams (teamID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.teamsPlayers
            ADD FOREIGN KEY (firstGameID)
            REFERENCES nhldb.games (gameID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.teamsPlayers
            ADD FOREIGN KEY (lastGameID)
            REFERENCES nhldb.games (gameID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.teamsPlayers
            ADD FOREIGN KEY (teamID)
            REFERENCES nhldb.teams (teamID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.teamsPlayers
            ADD FOREIGN KEY (seasonID)
            REFERENCES nhldb.seasons (seasonID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.teamsPlayers
            ADD FOREIGN KEY (playerID)
            REFERENCES nhldb. players (playerID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.gamePlayerStats
            ADD FOREIGN KEY (gameID)
            REFERENCES nhldb.games (gameID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.gamePlayerStats
            ADD FOREIGN KEY (playerID)
            REFERENCES nhldb. players (playerID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
        """,
        """ 
        ALTER TABLE IF EXISTS nhldb.gameResults
            ADD FOREIGN KEY (gameID)
            REFERENCES nhldb.games (gameID) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID
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