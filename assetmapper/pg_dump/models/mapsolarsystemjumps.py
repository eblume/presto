"""Model for Postgres dump of 'mapsolarsystemjumps' table"""
import sqlalchemy as sa


metadata = sa.MetaData()

mapsolarsystemjumps = sa.Table("mapsolarsystemjumps", metadata,
    sa.Column('fromsolarsystemid', sa.Integer),
    sa.Column('tosolarsystemid', sa.Integer),
    # Also from and to for region and constellation: not needed.
)
