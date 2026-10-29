"""remove school from client profiles

Revision ID: f1c7e3a9b5d2
Revises: e9b5d1f7a3c8
Create Date: 2026-10-29 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f1c7e3a9b5d2'
down_revision: Union[str, Sequence[str], None] = 'e9b5d1f7a3c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('client_profiles', 'school')


def downgrade() -> None:
    op.add_column('client_profiles', sa.Column('school', sa.String(length=150), nullable=True))
