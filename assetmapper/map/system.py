"Models and Views for solar systems in Eve Online"

import sqlalchemy as sa

from assetmapper.orm import Base


class System(Base):
    __tablename__ = 'systems'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    x = sa.Column(sa.Float)
    y = sa.Column(sa.Float)
    z = sa.Column(sa.Float)
