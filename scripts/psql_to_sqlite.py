#!/usr/bin/env python3

"""Connect and convert the PostgreSQL dump to a sqlite database useable by
assetmapper.

This script requires that the current data dump be already loaded on a local
postgresql database. At some point I may add command line options to this
script but since I'm likely to be the only guy using it (since the resulting
sqlite database is packaged in the repo)  instead all options are at the top
of this file, below this docstring.
"""

