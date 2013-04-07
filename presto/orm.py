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

Base = declarative_base()
orm_session = make_session()
