from nhldb_dropTables import drop_tables
from nhldb_createSchema import create_tables
from conferencesLoad import conferencesLoad
from divisionsLoad import divisionsLoad
from teamsLoad import teamsLoad
from gamesLoad import gamesLoad
from gameResultsLoad import gameResultsLoad
from playersLoad import playersLoad
from nhldb_createViews import create_views


def rebuild_nhldb():
# drop tables    
    drop_tables()

# create tables    
    create_tables()

# load tables    
    conferencesLoad()
    divisionsLoad()
    teamsLoad()
    gamesLoad()
    gameResultsLoad()
    playersLoad()

# create views
    create_views()

if __name__ == '__main__':
    rebuild_nhldb()
