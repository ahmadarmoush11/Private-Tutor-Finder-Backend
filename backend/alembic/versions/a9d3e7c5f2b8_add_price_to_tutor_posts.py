"""add price to tutor posts

Revision ID: a9d3e7c5f2b8
Revises: f8b2d5e7a4c1
Create Date: 2026-10-16 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a9d3e7c5f2b8'
down_revision: Union[str, Sequence[str], None] = 'f8b2d5e7a4c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


currency = sa.Enum('USD', 'LBP', name='currency')
price_unit = sa.Enum('hour', 'session', 'week', 'month', name='price_unit')


def upgrade() -> None:
    bind = op.get_bind()
    currency.create(bind, checkfirst=True)
    price_unit.create(bind, checkfirst=True)

    op.add_column('tutor_posts', sa.Column('price', sa.Numeric(12, 2), nullable=True))
    op.add_column('tutor_posts', sa.Column('currency', currency, nullable=True))
    op.add_column('tutor_posts', sa.Column('price_unit', price_unit, nullable=True))


def downgrade() -> None:
    op.drop_column('tutor_posts', 'price_unit')
    op.drop_column('tutor_posts', 'currency')
    op.drop_column('tutor_posts', 'price')

    bind = op.get_bind()
    price_unit.drop(bind, checkfirst=True)
    currency.drop(bind, checkfirst=True)
