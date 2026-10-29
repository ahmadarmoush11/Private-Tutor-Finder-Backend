"""remove grade from client profiles

Revision ID: e9b5d1f7a3c8
Revises: d7f3b9c5e1a6
Create Date: 2026-10-29 11:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e9b5d1f7a3c8'
down_revision: Union[str, Sequence[str], None] = 'd7f3b9c5e1a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('ck_client_profiles_grade_range', 'client_profiles', type_='check')
    op.drop_column('client_profiles', 'grade')


def downgrade() -> None:
    op.add_column('client_profiles', sa.Column('grade', sa.SmallInteger(), nullable=True))
    op.create_check_constraint(
        'ck_client_profiles_grade_range',
        'client_profiles',
        'grade BETWEEN 1 AND 12',
    )
