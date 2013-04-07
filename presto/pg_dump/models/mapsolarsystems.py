"""Model for Postgres dump of 'mapsolarsystems' table"""
import sqlalchemy as sa


metadata = sa.MetaData()

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
