presto
------

Swiss army knife package for application development for Eve Online.
by Erich Blume <blume.erich@gmail.com>

Quickstart
==========

Please note that this quickstart is not comprehensive! It's just a quick taste.

    >>> from presto.map.system import System
    >>> stacmon = System.by_name("Stacmon")
    >>> stacmon.region.name
    "Placid"
    >>> stacmon.constellation.name
    "Fislipesnes"
    >>> "Ostingele" in {x.name for x in stacmon.neighbors()}
    True

About
=====

`presto` aims to be an all-purpose tool for querying both online and offline
(game cache) data related to Eve Online. Presto is still in its infancy, but
in time it will support thing such as:

* Rich ORM-backed (sqlite) access to the game client data, including helper
  functions and normalization so that you get the data you need with no fuss.
* Heavily documented and tested code, so that you can get right to your project.
* Integrated API handlers that automatically link to the ORM client cache

What does this mean? It means that you can use presto to access all of the
offline and online data for Eve Online without having to worry about poorly
documented MSSQL databases or XML parsing.

What won't it do? Presto will not be an application itself - it won't handle
persistant storage of API keys, for instance. It won't include a ship fitting
tool either. But you can easily build a layer on top of Presto to do either of
those things, without having to worry about mucking around for game data about
items.

Documentation
=============

Documentation is currently being added, but you can generally get to the
majority of what matters by using help() on any modules, packages, or classes
defined by presto.

For a good introduction to the capabilities, see the `tests` folder.

Eventually, a 'Cookbook' will be added with examples of what presto can do.

Installation & Setup
====================

`python3 setup.py develop` will download the required packages and create a
development environment in the project folder. This is your best bet for now.

When the project is useful enough to warrant installing to the system path,
use `python3 setup.py install`. You may need to run that as a superuser.

presto has only been tested on OS X, but is being written to be as portable
as possible. Please file a bug report if you encounter any problems.

Tests
=====

Run `python3 setup.py nosetests` to establish the development environment,
download required packages, and run the entire test suite.

License
=======

`presto` is copyright Erich Blume, 2013.

Permission is given to self-license this software under the terms of the MIT
License, until such time as I include this license directly in the software.
I'm a bit lazy at the moment to do that. Maybe send it in a patch? Roughly
speaking, it's open source.
