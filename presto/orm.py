"Constants and global symbols needed for the ORM at run-time."

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from os.path import exists, dirname, sep


def make_session():
    """Create a Session object - a connection to the sqlite database will
    persist for as long as
    """
    data_file = "data_rev_1_1.sqlite"
    data_path = sep.join((dirname(__file__), data_file))
    if not exists(data_path):
        return None

    sqlite_path = "sqlite:///{}".format(data_path)
    engine = sa.create_engine(sqlite_path)
    Session = sa.orm.sessionmaker()
    Session.configure(bind=engine)

    return Session()


orm_session = make_session()


class NamedModel(object):
    "Mixin for models that have a 'name' field."

    @classmethod
    def by_name(cls, name):
        "Retrieve the instance of this model with the given name."
        return orm_session.query(cls).filter(cls.name == name).one()

    def __str__(self):
        return self.name


class Base(object):

    @classmethod
    def fetch_all(cls):
        "Fetch all objects of this type. Returns an iterator."
        return orm_session.query(cls).all()

Base = declarative_base(cls=Base)
