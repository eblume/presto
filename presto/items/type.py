"Models and views for Types (aka 'Items', except generic)"

from sqlalchemy import Integer, String, Float, Column, ForeignKey, Boolean

from presto.orm import Base, orm_session, NamedModel


class Type(Base, NamedModel):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    description = Column(String)
    mass = Column(Float)
    volume = Column(Float)
    portionsize = Column(Float)
    baseprice = Column(Float)
    published = Column(Boolean)
    market_group_id = Column(Integer, ForeignKey('marketgroups.id'))


class Group(Base, NamedModel):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    description = Column(String)
    manufacturable = Column(Boolean)
    recyclable = Column(Boolean)
    anchored = Column(Boolean)
    anchorable = Column(Boolean)
    fit_singleton = Column(Boolean)
    published = Column(Boolean)

    types = relationship("Type", backref="group")


class Category(Base, NamedModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    published = Column(Boolean)

    groups = relationship('Group', backref="category")


class MarketGroup(Base, NamedModel):
    __tablename__ = 'marketgroups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('marketgroups.id'), nullable=True)
    description = Column(String)

    types = relationship('Type', backref="marketgroup")
    subgroups = relationship('MarketGroup',
        backref=backref('parentgroup', remote_side=[id]))


