#!/usr/bin/env python3

from setuptools import setup, find_packages
from glob import glob

stuff = {
    'name': 'presto',
    'version': '0.1',
    'description': 'Eve Online all-purpose development package',
    'author': 'Erich Blume',
    'author_email': 'blume.erich@gmail.com',
    'packages': find_packages(),
    'scripts': glob('scripts/*'),
    'include_package_data': True,
    'install_requires': [
        'sqlalchemy==0.8.0',
        'psycopg2',
        'nose',
    ],
}

setup(**stuff)
