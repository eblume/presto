"""Model for Postgres dump of 'mapregions' table"""
import sqlalchemy as sa


metadata = sa.MetaData()

mapregions = sa.Table("mapregions", metadata,
    sa.Column('regionid', sa.Integer),
    sa.Column('regionname', sa.String),
    sa.Column('x', sa.Float),
    sa.Column('y', sa.Float),
    sa.Column('z', sa.Float),
    sa.Column('factionid', sa.Integer),
    sa.Column('radius', sa.Float),
)
