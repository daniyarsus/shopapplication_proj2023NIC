"""add is_recieved

Revision ID: 36c913fbdb3f
Revises: 845c3c82d7e0
Create Date: 2024-03-09 17:01:38.261150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36c913fbdb3f'
down_revision: Union[str, None] = '845c3c82d7e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
