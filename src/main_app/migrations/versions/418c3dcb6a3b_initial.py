"""initial

Revision ID: 418c3dcb6a3b
Revises: b12e57189392
Create Date: 2024-08-02 12:16:30.084166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '418c3dcb6a3b'
down_revision: Union[str, None] = 'b12e57189392'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('anime', 'start_date',
               existing_type=sa.DATE(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=False)
    op.alter_column('anime', 'end_date',
               existing_type=sa.DATE(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('anime', 'end_date',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.DATE(),
               existing_nullable=False)
    op.alter_column('anime', 'start_date',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.DATE(),
               existing_nullable=False)
    # ### end Alembic commands ###
