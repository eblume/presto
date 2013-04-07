"Models and Views for Constellations in Eve Online"

from sqlalchemy import Integer, String, Column, Float, ForeignKey
from sqlalchemy.orm import relationship

from presto.orm import Base


class Constellation(Base):
    __tablename__ = 'constellations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

    systems = relationship("System", backref="constellation")
    region_id = Column(Integer, ForeignKey('regions.id'))

