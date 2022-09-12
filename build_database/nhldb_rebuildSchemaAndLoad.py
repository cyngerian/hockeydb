from nhldb_dropTables import drop_tables
from nhldb_createSchema import create_tables
from seasonsLoad import seasonsLoad
from conferencesLoad import conferencesLoad
from divisionsLoad import divisionsLoad
from teamsLoad import teamsLoad
from gamesLoad import gamesLoad
from gameResultsLoad import gameResultsLoad
from playersLoad import playersLoad
from gameSkaterStatsLoad import gameSkaterStatsLoad
from gameGoalieStatsLoad import gameGoalieStatsLoad
from nhldb_createViews import create_views


def rebuild_nhldb():
# drop tables    
    drop_tables()
    print('---nhldb tables dropped---')

# create tables    
    create_tables()
    print('---nhldb tables created---')

# load tables    
    seasonsLoad()
    print('---seasons loaded into nhldb---')
    conferencesLoad()
    print('---conferenced loaded into nhldb---')
    divisionsLoad()
    print('---divisions loaded into nhldb---')
    teamsLoad()
    print('---teams loaded into nhldb---')
    gamesLoad()
    print('---games loaded into nhldb---')
    gameResultsLoad()
    print('---game results loaded into nhldb---')
    playersLoad()
    print('---players info loaded into nhldb---')
    gameSkaterStatsLoad()
    print('---game skater stats loaded into nhldb---')
    gameGoalieStatsLoad()
    print('---game goalie stats loaded into nhldb---')

# create views
    create_views()
    print('---nhldb views created---')
    print('---nhldb has been successfully rebuilt---')

if __name__ == '__main__':
    rebuild_nhldb()
