import sqlalchemy as sa

metadata = sa.MetaData()

mapregions = sa.Table("invtypes", metadata,
    sa.Column('typeid', sa.Integer),
    sa.Column('groupid', sa.Integer),
    sa.Column('typename', sa.String),
    sa.Column('description', sa.String),
    sa.Column('mass', sa.Float),
    sa.Column('volume', sa.Float),
    sa.Column('capacity', sa.Float),
    sa.Column('portionsize', sa.Integer),
    sa.Column('baseprice', sa.Float),
    sa.Column('published', sa.Integer),
    sa.Column('marketgroupid', sa.Integer),
)

mapconstellations = sa.Table("mapconstellations", metadata,
    sa.Column('regionid', sa.Integer),
    sa.Column('constellationid', sa.Integer),
    sa.Column('constellationname', sa.String, nullable=True),
    sa.Column('x', sa.Float),
    sa.Column('y', sa.Float),
    sa.Column('z', sa.Float),
    sa.Column('xMin', sa.Float),  # Note the unusual camelcase here
    sa.Column('xMax', sa.Float),  # and here
    sa.Column('ymin', sa.Float),
    sa.Column('ymax', sa.Float),
    sa.Column('zmin', sa.Float),
    sa.Column('zmax', sa.Float),
    # Omitted some crap we don't care about
    sa.Column('factionid', sa.Integer),
    sa.Column('radius', sa.Float),
)

mapregions = sa.Table("mapregions", metadata,
    sa.Column('regionid', sa.Integer),
    sa.Column('regionname', sa.String),
    sa.Column('x', sa.Float),
    sa.Column('y', sa.Float),
    sa.Column('z', sa.Float),
    sa.Column('factionid', sa.Integer),
    sa.Column('radius', sa.Float),
)

mapsolarsystemjumps = sa.Table("mapsolarsystemjumps", metadata,
    sa.Column('fromsolarsystemid', sa.Integer),
    sa.Column('tosolarsystemid', sa.Integer),
    # Also from and to for region and constellation: not needed.
)

mapsolarsystems = sa.Table("mapsolarsystems", metadata,
    sa.Column('regionid', sa.Integer),
    sa.Column('constellationid', sa.Integer),
    sa.Column('solarsystemid', sa.Integer, nullable=False),
    sa.Column('solarsystemname', sa.String, nullable=True),
    sa.Column('x', sa.Float),
    sa.Column('y', sa.Float),
    sa.Column('z', sa.Float),
    sa.Column('xMin', sa.Float),  # Note the unusual camelcase here
    sa.Column('xMax', sa.Float),  # and here
    sa.Column('ymin', sa.Float),
    sa.Column('ymax', sa.Float),
    sa.Column('zmin', sa.Float),
    sa.Column('zmax', sa.Float),
    # Omitted some crap we don't care about
    sa.Column('constellation', sa.Integer),
    sa.Column('security', sa.Float),
    sa.Column('factionid', sa.Integer),
    sa.Column('radius', sa.Float),
)
