"""initial

Revision ID: 71e48db355f1
Revises: 60fba79f57cb
Create Date: 2024-08-08 13:59:21.788392

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '71e48db355f1'
down_revision: Union[str, None] = '60fba79f57cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Manually check if the enum type exists and create it if not
    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'animeageratingenum') THEN
            CREATE TYPE animeageratingenum AS ENUM ('G', 'PG', 'R', 'R18');
        END IF;
    END $$;
    """)

    # Add the columns using the existing enum type
    age_rating_enum = postgresql.ENUM('G', 'PG', 'R', 'R18', name='animeageratingenum')
    op.add_column('anime', sa.Column('age_rating', age_rating_enum, nullable=False))
    op.add_column('anime', sa.Column('age_rating_guide', sqlmodel.sql.sqltypes.AutoString(), nullable=False))


def downgrade() -> None:
    # Drop the columns
    op.drop_column('anime', 'age_rating_guide')
    op.drop_column('anime', 'age_rating')

    # Optionally, drop the enum type (if you want to remove it during a downgrade)
    # op.execute("DROP TYPE IF EXISTS animeageratingenum")
