"Models and views for Types (aka 'Items', except generic)"

from sqlalchemy import Integer, String, Float, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
try:
    # Python 3
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib2 import urlopen
    from urllib import urlencode
import xml.etree.ElementTree as ET

from presto.orm import Base, NamedModel


class Type(Base, NamedModel):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    description = Column(String)
    mass = Column(Float)
    volume = Column(Float)
    capacity = Column(Float)
    portionsize = Column(Float)
    baseprice = Column(Float)
    published = Column(Boolean)
    marketgroup_id = Column(Integer, ForeignKey('marketgroups.id'))

    price_cache = None

    def jita_price(self):
        "Query eve-central for Jita price data for this item."
        if self.price_cache:
            return self.price_cache

        data = {
            "typeid": self.id,
            "usesystem": 30000142,  # Jita
        }
        endpoint = "http://api.eve-central.com/api/marketstat"
        response = urlopen(endpoint, urlencode(data).encode("UTF-8"))
        root = ET.fromstring(response.read())
        price = float(root[0][0][0][1].text)
        self.price_cache = price
        return price


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


