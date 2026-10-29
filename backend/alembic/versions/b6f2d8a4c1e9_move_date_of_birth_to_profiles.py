"""move date_of_birth from users to client and tutor profiles

Revision ID: b6f2d8a4c1e9
Revises: a3d8f2c6e4b1
Create Date: 2026-10-29 12:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b6f2d8a4c1e9'
down_revision: Union[str, Sequence[str], None] = 'a3d8f2c6e4b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PROFILE_TABLES = ['client_profiles', 'tutor_profiles']


def upgrade() -> None:
    for table in PROFILE_TABLES:
        op.add_column(table, sa.Column('date_of_birth', sa.Date(), nullable=True))
        op.execute(
            f'UPDATE {table} SET date_of_birth = users.date_of_birth '
            f'FROM users WHERE users.id = {table}.user_id'
        )
    op.drop_column('users', 'date_of_birth')


def downgrade() -> None:
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True))
    for table in PROFILE_TABLES:
        op.execute(
            f'UPDATE users SET date_of_birth = {table}.date_of_birth '
            f'FROM {table} WHERE {table}.user_id = users.id AND users.date_of_birth IS NULL'
        )
        op.drop_column(table, 'date_of_birth')
