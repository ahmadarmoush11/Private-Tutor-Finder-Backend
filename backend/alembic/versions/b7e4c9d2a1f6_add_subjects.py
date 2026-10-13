"""add subjects

Revision ID: b7e4c9d2a1f6
Revises: a3d5f8c21b47
Create Date: 2026-10-13 11:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b7e4c9d2a1f6'
down_revision: Union[str, Sequence[str], None] = 'a3d5f8c21b47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'subjects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index(op.f('ix_subjects_id'), 'subjects', ['id'], unique=False)

    op.create_table(
        'client_post_subjects',
        sa.Column('client_post_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['client_post_id'], ['client_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('client_post_id', 'subject_id'),
    )
    op.create_index(
        op.f('ix_client_post_subjects_subject_id'),
        'client_post_subjects',
        ['subject_id'],
        unique=False,
    )

    op.create_table(
        'tutor_post_subjects',
        sa.Column('tutor_post_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tutor_post_id'], ['tutor_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('tutor_post_id', 'subject_id'),
    )
    op.create_index(
        op.f('ix_tutor_post_subjects_subject_id'),
        'tutor_post_subjects',
        ['subject_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_tutor_post_subjects_subject_id'), table_name='tutor_post_subjects')
    op.drop_table('tutor_post_subjects')
    op.drop_index(op.f('ix_client_post_subjects_subject_id'), table_name='client_post_subjects')
    op.drop_table('client_post_subjects')
    op.drop_index(op.f('ix_subjects_id'), table_name='subjects')
    op.drop_table('subjects')
