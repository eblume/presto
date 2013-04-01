#!/usr/bin/env python3

"""Connect and convert the PostgreSQL dump to a sqlite database useable by
assetmapper.

This script requires that the current data dump be already loaded on a local
postgresql database. At some point I may add command line options to this
script but since I'm likely to be the only guy using it (since the resulting
sqlite database is packaged in the repo)  instead all options are at the top
of this file, below this docstring.
"""
### CONFIGURATION:
PG_USER = "eblume"
PG_SERVER = "localhost"
PG_DATABASE = "eve_rev_11"

### END CONFIGURATION

### IMPORTS
import sqlalchemy as sa

from assetmapper.orm import Base
from assetmapper.pg_dump.models import mapsolarsystems

### GLOBALS
PG_CONNECTION = "postgres://{}@{}/{}".format(PG_USER, PG_SERVER, PG_DATABASE)
SQLITE_CONNECTION = "sqlite:///{}.sqlite".format(PG_DATABASE)


def main():
    pg_conn = sa.create_engine(PG_CONNECTION)

    sqlite_conn = sa.create_engine(SQLITE_CONNECTION)
    Session = sa.orm.sessionmaker()
    Session.configure(bind=sqlite_conn)
    sqlite_sess = Session()

    # Create all the tables we will be populating
    Base.metadata.create_all(sqlite_conn)

    # Populate System
    sqlite_sess.add_all(mapsolarsystems.all_systems(pg_conn))

    # Flush to disk
    sqlite_sess.commit()


if __name__ == "__main__":
    main()
