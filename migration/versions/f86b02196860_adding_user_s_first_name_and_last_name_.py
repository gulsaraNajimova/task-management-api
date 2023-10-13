"""Adding user's first name and last name to Users table

Revision ID: f86b02196860
Revises: 
Create Date: 2023-10-10 22:35:30.624069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f86b02196860'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("users", sa.Column("firstname", sa.String(), nullable=True))
    op.add_column("users", sa.Column("lastname", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "firstname")
    op.drop_column("users", "lastname")