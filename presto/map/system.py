"Models and Views for solar systems in Eve Online"

from sqlalchemy import Integer, String, Float, Column, ForeignKey, or_, and_

from presto.orm import Base, orm_session, NamedModel


class System(Base, NamedModel):
    __tablename__ = 'systems'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    constellation_id = Column(Integer, ForeignKey('constellations.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))

    def neighbors(self):
        "Return an iterable (cursor) of the neighbors of this system"
        return orm_session.query(System).filter(
            or_(
                System.id.in_(orm_session.query(Jump.from_system).filter(
                    Jump.to_system == self.id
                )),
                System.id.in_(orm_session.query(Jump.to_system).filter(
                    Jump.from_system == self.id
                ))
            )
        )


class Jump(Base):
    __tablename__ = 'jumps'

    id = Column(Integer, primary_key=True)
    from_system = Column(Integer, ForeignKey('systems.id'))
    to_system = Column(Integer, ForeignKey('systems.id'))
