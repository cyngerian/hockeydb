from drop_tables import drop_tables
from create_nhldb import create_tables
from conferencesLoad import conferencesLoad
from divisionsLoad import divisionsLoad
from teamsLoad import teamsLoad


def rebuild_nhldb():
    drop_tables()
    create_tables()
    conferencesLoad()
    divisionsLoad()
    teamsLoad()


if __name__ == '__main__':
    rebuild_nhldb()
