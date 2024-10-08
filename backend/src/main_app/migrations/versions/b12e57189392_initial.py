"""initial

Revision ID: b12e57189392
Revises: 
Create Date: 2024-08-02 12:09:10.642771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b12e57189392'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anime',
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('synopsis', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('poster_image', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('status', sa.Enum('CURRENT', 'FINISHED', 'TBA', 'UPCOMING', 'UNRELEASED', name='animestatusenum'), nullable=False),
    sa.Column('episode_count', sa.Integer(), nullable=False),
    sa.Column('show_type', sa.Enum('ONA', 'OVA', 'TV', 'MOVIE', 'MUSIC', 'SPECIAL', name='animeshowtypeenum'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'USER', name='roleenum'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('anime')
    # ### end Alembic commands ###
