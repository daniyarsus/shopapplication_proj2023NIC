"""add column photo to User

Revision ID: 90f4d5a55e34
Revises: a9b0ef3aaed3
Create Date: 2024-03-13 18:05:33.077242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90f4d5a55e34'
down_revision: Union[str, None] = 'a9b0ef3aaed3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
