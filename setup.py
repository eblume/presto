#!/usr/bin/env python3

import os
import sys
import glob

# distribute stuff
from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

# The following is taken from python.org:
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'presto',
    version = 0.2,
    packages = find_packages(),
    scripts = glob.glob(os.path.join(os.path.dirname(__file__),'scripts/*')),
    include_package_data = True,

    # Required packages for installation
    install_requires = [
        'docutils>=0.3', 
        'sqlalchemy',
        'psycopg2',
    ],

    setup_requires = [
        'nose>=1.0',
        'coverage>=3.5.1',
    ],

    author = 'Erich Blume',
    author_email = 'blume.erich@gmail.com',
    description = ('Eve Online development swiss army knife.'),
    url = 'https://github.com/eblume/presto',
    download_url='https://github.com/eblume/presto/tarball/master',
    long_description = read('README.md'),
)
