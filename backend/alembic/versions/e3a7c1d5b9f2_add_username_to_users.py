"""add username to users

Revision ID: e3a7c1d5b9f2
Revises: d1e7b3f9a2c6
Create Date: 2026-10-18 11:30:00.000000

"""
import secrets
import string
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e3a7c1d5b9f2'
down_revision: Union[str, Sequence[str], None] = 'd1e7b3f9a2c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ALPHABET = string.ascii_lowercase + string.digits


def _random_username(taken: set[str]) -> str:
    while True:
        username = 'user_' + ''.join(secrets.choice(ALPHABET) for _ in range(8))
        if username not in taken:
            taken.add(username)
            return username


def upgrade() -> None:
    op.add_column('users', sa.Column('username', sa.String(length=30), nullable=True))

    connection = op.get_bind()
    users = sa.table('users', sa.column('id', sa.Integer), sa.column('username', sa.String))
    user_ids = connection.execute(sa.select(users.c.id)).scalars().all()
    taken: set[str] = set()
    for user_id in user_ids:
        connection.execute(
            users.update()
            .where(users.c.id == user_id)
            .values(username=_random_username(taken))
        )

    op.alter_column('users', 'username', nullable=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_column('users', 'username')
