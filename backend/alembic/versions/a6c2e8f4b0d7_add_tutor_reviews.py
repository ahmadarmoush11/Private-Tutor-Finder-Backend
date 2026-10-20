"""add tutor reviews

Revision ID: a6c2e8f4b0d7
Revises: f4b8d2e6a1c3
Create Date: 2026-10-19 20:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a6c2e8f4b0d7'
down_revision: Union[str, Sequence[str], None] = 'f4b8d2e6a1c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tutor_reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lesson_request_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.SmallInteger(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('rating BETWEEN 1 AND 5', name='ck_tutor_reviews_rating_range'),
        sa.ForeignKeyConstraint(['lesson_request_id'], ['lesson_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_tutor_reviews_id'), 'tutor_reviews', ['id'])
    op.create_index(
        op.f('ix_tutor_reviews_lesson_request_id'),
        'tutor_reviews',
        ['lesson_request_id'],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_tutor_reviews_lesson_request_id'), table_name='tutor_reviews')
    op.drop_index(op.f('ix_tutor_reviews_id'), table_name='tutor_reviews')
    op.drop_table('tutor_reviews')
