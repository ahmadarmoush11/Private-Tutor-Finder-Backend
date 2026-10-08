"""add lesson location to client posts

Revision ID: 7c4e2a9b1f30
Revises: 153ab6850d85
Create Date: 2026-10-08 21:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7c4e2a9b1f30'
down_revision: Union[str, Sequence[str], None] = '153ab6850d85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


lesson_location = sa.Enum('client_home', 'tutor_home', 'any', name='lesson_location')


def upgrade() -> None:
    lesson_location.create(op.get_bind(), checkfirst=True)
    op.add_column(
        'client_posts',
        sa.Column('lesson_location', lesson_location, server_default='any', nullable=False),
    )
    op.create_index(
        op.f('ix_client_posts_lesson_location'),
        'client_posts',
        ['lesson_location'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_client_posts_lesson_location'), table_name='client_posts')
    op.drop_column('client_posts', 'lesson_location')
    lesson_location.drop(op.get_bind(), checkfirst=True)
