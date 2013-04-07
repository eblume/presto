#!/usr/bin/env python3

"""Connect and convert the PostgreSQL dump to a sqlite database useable by
presto.

This script requires that the current data dump be already loaded on a local
postgresql database. At some point I may add command line options to this
script but since I'm likely to be the only guy using it (since the resulting
sqlite database is packaged in the repo)  instead all options are at the top
of this file, below this docstring.

The output file is called "{PG_DATABASE}.sqlite" and is dumped in the current
working directory.
"""
### CONFIGURATION:
PG_USER = "eblume"
PG_SERVER = "localhost"
PG_DATABASE = "eve_rev_11"

### END CONFIGURATION

### IMPORTS
import sqlalchemy as sa

from presto.orm import Base
from presto.pg_dump.models.mapsolarsystems import mapsolarsystems
from presto.pg_dump.models.mapconstellations import mapconstellations
from presto.pg_dump.models.mapregions import mapregions
from presto.pg_dump.models.mapsolarsystemjumps import mapsolarsystemjumps
from presto.map.system import System, Jump
from presto.map.constellation import Constellation
from presto.map.region import Region

### GLOBALS
PG_CONNECTION = "postgres://{}@{}/{}".format(PG_USER, PG_SERVER, PG_DATABASE)
SQLITE_CONNECTION = "sqlite:///{}.sqlite".format(PG_DATABASE)


def all_regions(conn):
    for region in fetch(conn, mapregions.select()):
        yield Region(
            id=region.regionid,
            name=region.regionname,
            x=region.x,
            y=region.y,
            z=region.z,
        )


def all_constellations(conn):
    for constellation in fetch(conn, mapconstellations.select()):
        yield Constellation(
            id=constellation.constellationid,
            name=constellation.constellationname,
            x=constellation.x,
            y=constellation.y,
            z=constellation.z,
            region_id=constellation.regionid,
        )


def all_systems(conn):
    for system in fetch(conn, mapsolarsystems.select()):
        yield System(
            id=system.solarsystemid,
            name=system.solarsystemname,
            x=system.x,
            y=system.y,
            z=system.z,
            constellation_id=system.constellationid,
            region_id=system.regionid,
        )


def all_jumps(conn):
    for jump in fetch(conn, mapsolarsystemjumps.select()):
        pair = sorted([jump.fromsolarsystemid, jump.tosolarsystemid])
        yield Jump(from_system=pair[0], to_system=pair[1])


def fetch(conn, query):
    with conn.begin() as trans:
        return trans.execute(query)


def main():
    pg_conn = sa.create_engine(PG_CONNECTION)

    sqlite_conn = sa.create_engine(SQLITE_CONNECTION)
    Session = sa.orm.sessionmaker()
    Session.configure(bind=sqlite_conn)
    sqlite_sess = Session()

    # Create all the tables we will be populating
    Base.metadata.create_all(sqlite_conn)

    # Populate Systems
    sqlite_sess.add_all(all_systems(pg_conn))

    # Populate Constellations
    sqlite_sess.add_all(all_constellations(pg_conn))

    # Populate Regions
    sqlite_sess.add_all(all_regions(pg_conn))

    # Populate Jump network
    sqlite_sess.add_all(all_jumps(pg_conn))

    # Flush to disk
    sqlite_sess.commit()


if __name__ == "__main__":
    main()
