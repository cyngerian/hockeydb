import psycopg2
from config import config

def create_views():
    """ create views in the nhldb database"""
    commands = (
        """
        CREATE VIEW nhldb."gameResult_scores"
        AS
        with gameResult_scores as 
        (
        select 
            g.gameid
            , g.dateTime
            , ht.teamid as homeTeamId
            , ht.abbreviation as homeTeam
            , gr.homeTeamScore
            , at.teamid as awayTeamId
            , at.abbreviation as awayTeam
            , gr.awayTeamScore
            , case 
                when hometeamscore > awayteamscore then ht.abbreviation
                when awayteamscore > hometeamscore then at.abbreviation
                else 'na'
            end as winTeam
            , gr.endtype
        from nhldb.games g
        inner join nhldb.teams ht
                on g.hometeamid = ht.teamid
        inner join nhldb.divisions hd
                on ht.divisionid = hd.divisionid
        inner join nhldb.conferences hc
                on hd.conferenceid = hc.conferenceid
        inner join nhldb.teams at
                on g.awayteamid = at.teamid
        inner join nhldb.divisions ad
                on at.divisionid = ad.divisionid
        inner join nhldb.conferences ac
                on ad.conferenceid = ac.conferenceid
        inner join nhldb.gameResults gr
                on g.gameid = gr.gameid
        where g.status = 'Final'
        )
        select * 
        from gameResult_scores
        order by dateTime asc;

        ALTER TABLE nhldb."gameResult_scores"
            OWNER TO postgres;
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(commands)
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
    create_views()