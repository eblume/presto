"Models and Views for Regions in Eve Online"

from sqlalchemy import Integer, String, Column, Float
from sqlalchemy.orm import relationship

from presto.orm import Base, NamedModel


class Region(Base, NamedModel):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

    systems = relationship("System", backref="region")
    constellations = relationship("Constellation", backref="region")
