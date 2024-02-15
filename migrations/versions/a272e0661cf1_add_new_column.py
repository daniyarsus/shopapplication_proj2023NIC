"""add new column

Revision ID: a272e0661cf1
Revises: b0af2e359d3c
Create Date: 2024-01-31 00:59:23.474697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a272e0661cf1'
down_revision: Union[str, None] = 'b0af2e359d3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('foods_id', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('payments', sa.Column('sets_id', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.drop_index('ix_payments_products_id', table_name='payments')
    op.create_index(op.f('ix_payments_foods_id'), 'payments', ['foods_id'], unique=False)
    op.create_index(op.f('ix_payments_sets_id'), 'payments', ['sets_id'], unique=False)
    op.drop_column('payments', 'products_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('products_id', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_payments_sets_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_foods_id'), table_name='payments')
    op.create_index('ix_payments_products_id', 'payments', ['products_id'], unique=False)
    op.drop_column('payments', 'sets_id')
    op.drop_column('payments', 'foods_id')
    # ### end Alembic commands ###