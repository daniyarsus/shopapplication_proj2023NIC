"""add column is_received to Payment

Revision ID: 845c3c82d7e0
Revises: b6625cd32d78
Create Date: 2024-03-08 23:40:29.124002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '845c3c82d7e0'
down_revision: Union[str, None] = 'b6625cd32d78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
