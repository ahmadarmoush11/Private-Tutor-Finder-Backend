"""tutor reviews link client and tutor instead of lesson request

Revision ID: b8d4f0a2c6e9
Revises: a6c2e8f4b0d7
Create Date: 2026-10-20 11:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b8d4f0a2c6e9'
down_revision: Union[str, Sequence[str], None] = 'a6c2e8f4b0d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    ]


def upgrade() -> None:
    op.drop_table('tutor_reviews')

    op.create_table(
        'tutor_reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('tutor_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.SmallInteger(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        *_timestamps(),
        sa.CheckConstraint('rating BETWEEN 1 AND 5', name='ck_tutor_reviews_rating_range'),
        sa.ForeignKeyConstraint(['client_id'], ['client_profiles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutor_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('client_id', 'tutor_id', name='uq_tutor_reviews_client_id_tutor_id'),
    )
    op.create_index(op.f('ix_tutor_reviews_id'), 'tutor_reviews', ['id'])
    op.create_index(op.f('ix_tutor_reviews_client_id'), 'tutor_reviews', ['client_id'])
    op.create_index(op.f('ix_tutor_reviews_tutor_id'), 'tutor_reviews', ['tutor_id'])


def downgrade() -> None:
    op.drop_table('tutor_reviews')

    op.create_table(
        'tutor_reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lesson_request_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.SmallInteger(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        *_timestamps(),
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
