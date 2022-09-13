import psycopg2
from config import config

sql = ("""
        insert into nhldb.teamsplayers
        select 
            playerid
            , teamid
            , seasonid
            , firstgameid
            , lastgameid
            , gamesplayed
            , row_number () over (partition by seasonid, playerid order by firstgameid asc) as stintnumber
        from (
            select
                gam.seasonid
                , gss.playerid
                , gss.teamid
                , count(gam.gameid) as gamesplayed
                , min(gam.gameid) as firstgameid
                , max(gam.gameid) as lastgameid
            from nhldb.gameskaterstats gss
            inner join nhldb.games gam
                    on gss.gameid = gam.gameid
            inner join nhldb.players plr
                    on gss.playerid = plr.playerid
            group by
                gam.seasonid
                , gss.playerid
                , gss.teamid
            ) a
      """)

def teamsPlayersCreateTable():
    """ creates teamsPlayers table in nhldb database"""
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql)
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
    teamsPlayersCreateTable()