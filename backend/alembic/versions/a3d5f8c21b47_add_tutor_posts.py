"""add tutor posts

Revision ID: a3d5f8c21b47
Revises: 7c4e2a9b1f30
Create Date: 2026-10-10 14:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'a3d5f8c21b47'
down_revision: Union[str, Sequence[str], None] = '7c4e2a9b1f30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


lesson_location = postgresql.ENUM(
    'client_home', 'tutor_home', 'any', name='lesson_location', create_type=False
)
post_status = postgresql.ENUM('active', 'inactive', name='post_status', create_type=False)


def upgrade() -> None:
    op.create_table(
        'tutor_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tutor_id', sa.Integer(), nullable=False),
        sa.Column('lesson_location', lesson_location, server_default='any', nullable=False),
        sa.Column('status', post_status, server_default='active', nullable=False),
        sa.Column('location', sa.String(length=150), nullable=True),
        sa.Column('address_details', sa.String(length=255), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutor_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_tutor_posts_id'), 'tutor_posts', ['id'], unique=False)
    op.create_index(op.f('ix_tutor_posts_tutor_id'), 'tutor_posts', ['tutor_id'], unique=False)
    op.create_index(op.f('ix_tutor_posts_lesson_location'), 'tutor_posts', ['lesson_location'], unique=False)
    op.create_index(op.f('ix_tutor_posts_status'), 'tutor_posts', ['status'], unique=False)

    op.create_table(
        'tutor_post_class_levels',
        sa.Column('tutor_post_id', sa.Integer(), nullable=False),
        sa.Column('class_level_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tutor_post_id'], ['tutor_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['class_level_id'], ['class_levels.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('tutor_post_id', 'class_level_id'),
    )
    op.create_index(
        op.f('ix_tutor_post_class_levels_class_level_id'),
        'tutor_post_class_levels',
        ['class_level_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_tutor_post_class_levels_class_level_id'), table_name='tutor_post_class_levels')
    op.drop_table('tutor_post_class_levels')
    op.drop_index(op.f('ix_tutor_posts_status'), table_name='tutor_posts')
    op.drop_index(op.f('ix_tutor_posts_lesson_location'), table_name='tutor_posts')
    op.drop_index(op.f('ix_tutor_posts_tutor_id'), table_name='tutor_posts')
    op.drop_index(op.f('ix_tutor_posts_id'), table_name='tutor_posts')
    op.drop_table('tutor_posts')
