"""change owner_id data type in tasks model

Revision ID: 9ed035c6635a
Revises: f86b02196860
Create Date: 2024-01-16 10:41:45.708171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9ed035c6635a'
down_revision: Union[str, None] = 'f86b02196860'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('tasks', 'owner_id', type_=postgresql.INTEGER, using='owner_id::int')


def downgrade():
    op.alter_column('tasks', 'owner_id', type_=sa.Integer)

