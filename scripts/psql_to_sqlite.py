#!/usr/bin/env python

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
import sys

from presto.orm import Base
import presto.pg_dump.tables as pg
from presto.map import System, Jump, Constellation, Region
from presto.items import Type, Group, Category, MarketGroup

### GLOBALS
PG_CONNECTION = "postgres://{}@{}/{}"
SQLITE_CONNECTION = "sqlite:///{}"


def all_marketgroups(conn):
    for mg in fetch(conn, pg.invmarketgroups):
        yield MarketGroup(
            id=mg.marketgroupid,
            name=mg.marketgroupname.strip(),  # Strip 'Hull & Armor '
            description=mg.description,
            parent_id=mg.parentgroupid,
        )


def all_categories(conn):
    for cat in fetch(conn, pg.invcategories):
        yield Category(
            id=cat.categoryid,
            name=cat.categoryname,
            description=cat.description,
            published=(cat.published == 1),
        )


def all_groups(conn):
    for group in fetch(conn, pg.invgroups):
        yield Group(
            id=group.groupid,
            name=group.groupname,
            category_id=group.categoryid,
            description=group.description,
            manufacturable=(group.allowmanufacture == 1),
            recyclable=(group.allowrecycler == 1),
            anchored=(group.anchored == 1),
            anchorable=(group.anchorable == 1),
            fit_singleton=(group.fittablenonsingleton != 1),
            published=(group.published == 1)
        )


def all_types(conn):
    for item in fetch(conn, pg.invtypes):
        yield Type(
            id=item.typeid,
            group_id=item.groupid,
            name=item.typename,
            description=item.description,
            mass=item.mass,
            volume=item.volume,
            capacity=item.capacity,
            portionsize=item.portionsize,
            baseprice=item.baseprice,
            published=(item.published == 1),
            marketgroup_id=item.marketgroupid,
        )


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
    if len(sys.argv) == 2:
        sconn = SQLITE_CONNECTION.format(sys.argv[1])
    elif len(sys.argv) == 1:
        sconn = SQLITE_CONNECTION.format(PG_DATABASE + ".sqlite")
    else:
        print("Please specify the output file name.")
        sys.exit(1)

    pg_conn = sa.create_engine(
        PG_CONNECTION.format(PG_USER, PG_SERVER, PG_DATABASE))
    sqlite_conn = sa.create_engine(sconn)
    Session = sa.orm.sessionmaker()
    Session.configure(bind=sqlite_conn)
    sqlite_sess = Session()

    # Create all the tables we will be populating
    Base.metadata.create_all(sqlite_conn)

    def populate(func):
        sqlite_sess.add_all(func(pg_conn))

    # Populate the map data
    populate(all_systems)
    populate(all_constellations)
    populate(all_regions)
    populate(all_jumps)

    # Populate the item data
    populate(all_marketgroups)
    populate(all_categories)
    populate(all_groups)
    populate(all_types)

    # Flush to disk
    sqlite_sess.commit()


if __name__ == "__main__":
    main()
