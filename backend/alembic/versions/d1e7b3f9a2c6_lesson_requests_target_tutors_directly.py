"""lesson requests target tutors directly instead of tutor posts

Revision ID: d1e7b3f9a2c6
Revises: c5d9a2e7f3b1
Create Date: 2026-10-17 12:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'd1e7b3f9a2c6'
down_revision: Union[str, Sequence[str], None] = 'c5d9a2e7f3b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


lesson_location = postgresql.ENUM(
    'client_home', 'tutor_home', 'any', name='lesson_location', create_type=False
)


def upgrade() -> None:
    op.execute('DELETE FROM lesson_requests')
    op.drop_column('lesson_requests', 'tutor_post_id')

    op.add_column('lesson_requests', sa.Column('tutor_id', sa.Integer(), nullable=False))
    op.add_column('lesson_requests', sa.Column('class_level_id', sa.Integer(), nullable=False))
    op.add_column(
        'lesson_requests',
        sa.Column('lesson_location', lesson_location, server_default='any', nullable=False),
    )
    op.add_column('lesson_requests', sa.Column('message', sa.Text(), nullable=True))

    op.create_foreign_key(
        'lesson_requests_tutor_id_fkey', 'lesson_requests', 'tutor_profiles',
        ['tutor_id'], ['id'], ondelete='CASCADE',
    )
    op.create_foreign_key(
        'lesson_requests_class_level_id_fkey', 'lesson_requests', 'class_levels',
        ['class_level_id'], ['id'], ondelete='RESTRICT',
    )
    op.create_index('ix_lesson_requests_tutor_id', 'lesson_requests', ['tutor_id'])
    op.create_index('ix_lesson_requests_class_level_id', 'lesson_requests', ['class_level_id'])
    op.create_index(
        'uq_lesson_requests_pending',
        'lesson_requests',
        ['client_id', 'tutor_id'],
        unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )

    op.create_table(
        'lesson_request_subjects',
        sa.Column('lesson_request_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['lesson_request_id'], ['lesson_requests.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('lesson_request_id', 'subject_id'),
    )
    op.create_index(
        op.f('ix_lesson_request_subjects_subject_id'),
        'lesson_request_subjects',
        ['subject_id'],
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_lesson_request_subjects_subject_id'),
        table_name='lesson_request_subjects',
    )
    op.drop_table('lesson_request_subjects')
    op.execute('DELETE FROM lesson_requests')
    op.drop_index('uq_lesson_requests_pending', table_name='lesson_requests')
    op.drop_column('lesson_requests', 'message')
    op.drop_column('lesson_requests', 'lesson_location')
    op.drop_column('lesson_requests', 'class_level_id')
    op.drop_column('lesson_requests', 'tutor_id')

    op.add_column('lesson_requests', sa.Column('tutor_post_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'lesson_requests_tutor_post_id_fkey', 'lesson_requests', 'tutor_posts',
        ['tutor_post_id'], ['id'], ondelete='CASCADE',
    )
    op.create_index('ix_lesson_requests_tutor_post_id', 'lesson_requests', ['tutor_post_id'])
