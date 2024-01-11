"""upd tables

Revision ID: 0a87b233c3b5
Revises: 4a6ab7fedd84
Create Date: 2024-01-11 17:03:23.000697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a87b233c3b5'
down_revision: Union[str, None] = '4a6ab7fedd84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('food_sets', sa.Column('price', sa.Integer(), nullable=True))
    op.add_column('food_sets', sa.Column('image_url', sa.String(), nullable=True))
    op.create_index(op.f('ix_food_sets_price'), 'food_sets', ['price'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_food_sets_price'), table_name='food_sets')
    op.drop_column('food_sets', 'image_url')
    op.drop_column('food_sets', 'price')
    # ### end Alembic commands ###
