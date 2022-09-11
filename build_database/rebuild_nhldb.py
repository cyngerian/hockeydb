from drop_tables import drop_tables
from create_nhldb import create_tables
from conferencesLoad import conferencesLoad
from divisionsLoad import divisionsLoad
from teamsLoad import teamsLoad
from gamesLoad import gamesLoad
from gameResultsLoad import gameResultsLoad
from playersLoad import playersLoad
from create_nhldb_views import create_views


def rebuild_nhldb():
    drop_tables()
    create_tables()
    conferencesLoad()
    divisionsLoad()
    teamsLoad()
    gamesLoad()
    gameResultsLoad()
    playersLoad()

    create_views()

if __name__ == '__main__':
    rebuild_nhldb()
