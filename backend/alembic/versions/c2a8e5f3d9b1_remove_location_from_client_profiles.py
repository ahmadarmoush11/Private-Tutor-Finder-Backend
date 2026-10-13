"""remove location from client profiles

Revision ID: c2a8e5f3d9b1
Revises: b7e4c9d2a1f6
Create Date: 2026-10-13 12:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c2a8e5f3d9b1'
down_revision: Union[str, Sequence[str], None] = 'b7e4c9d2a1f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('client_profiles', 'location')


def downgrade() -> None:
    op.add_column(
        'client_profiles',
        sa.Column('location', sa.String(length=150), nullable=True),
    )
