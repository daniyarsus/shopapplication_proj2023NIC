"""delete columns in Emplpyee

Revision ID: a9b0ef3aaed3
Revises: 36c913fbdb3f
Create Date: 2024-03-12 21:21:57.514557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9b0ef3aaed3'
down_revision: Union[str, None] = '36c913fbdb3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
