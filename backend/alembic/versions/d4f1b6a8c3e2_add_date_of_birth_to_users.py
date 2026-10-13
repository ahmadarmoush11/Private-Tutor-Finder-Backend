"""add date of birth to users

Revision ID: d4f1b6a8c3e2
Revises: c2a8e5f3d9b1
Create Date: 2026-10-13 12:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd4f1b6a8c3e2'
down_revision: Union[str, Sequence[str], None] = 'c2a8e5f3d9b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'date_of_birth')
