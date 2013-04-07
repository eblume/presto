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
PG_DATABASE = "presto"

### END CONFIGURATION

### IMPORTS
import sqlalchemy as sa

from presto.orm import Base
import prest.pg_dump as pg
from presto.map import System, Jump, Constellation, Region

### GLOBALS
PG_CONNECTION = "postgres://{}@{}/{}".format(PG_USER, PG_SERVER, PG_DATABASE)
SQLITE_CONNECTION = "sqlite:///{}.sqlite".format(PG_DATABASE)


def all_regions(conn):
    for region in fetch(conn, pg.mapregions):
        yield Region(
            id=region.regionid,
            name=region.regionname,
            x=region.x,
            y=region.y,
            z=region.z,
        )


def all_constellations(conn):
    for constellation in fetch(conn, pg.mapconstellations):
        yield Constellation(
            id=constellation.constellationid,
            name=constellation.constellationname,
            x=constellation.x,
            y=constellation.y,
            z=constellation.z,
            region_id=constellation.regionid,
        )


def all_systems(conn):
    for system in fetch(conn, pg.mapsolarsystems):
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
    for jump in fetch(conn, pg.mapsolarsystemjumps):
        pair = sorted([jump.fromsolarsystemid, jump.tosolarsystemid])
        yield Jump(from_system=pair[0], to_system=pair[1])


def fetch(conn, model):
    with conn.begin() as trans:
        return trans.execute(model.select())


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
