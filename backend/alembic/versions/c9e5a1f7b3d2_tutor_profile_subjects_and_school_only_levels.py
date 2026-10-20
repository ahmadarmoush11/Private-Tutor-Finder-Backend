"""add subjects and class levels to tutor profiles, remove higher education

Revision ID: c9e5a1f7b3d2
Revises: b8d4f0a2c6e9
Create Date: 2026-10-20 14:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c9e5a1f7b3d2'
down_revision: Union[str, Sequence[str], None] = 'b8d4f0a2c6e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


HIGHER_EDUCATION_LEVELS = (
    "SELECT id FROM class_levels WHERE level = 'higher_education'"
)


def _create_link_table(name: str, column: str, target: str) -> None:
    op.create_table(
        name,
        sa.Column('tutor_profile_id', sa.Integer(), nullable=False),
        sa.Column(column, sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tutor_profile_id'], ['tutor_profiles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint([column], [f'{target}.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('tutor_profile_id', column),
    )
    op.create_index(op.f(f'ix_{name}_{column}'), name, [column])


def upgrade() -> None:
    _create_link_table('tutor_profile_class_levels', 'class_level_id', 'class_levels')
    _create_link_table('tutor_profile_subjects', 'subject_id', 'subjects')

    op.execute(f'DELETE FROM lesson_requests WHERE class_level_id IN ({HIGHER_EDUCATION_LEVELS})')
    op.execute(f'DELETE FROM client_posts WHERE class_level_id IN ({HIGHER_EDUCATION_LEVELS})')
    op.execute(
        f'DELETE FROM tutor_post_class_levels WHERE class_level_id IN ({HIGHER_EDUCATION_LEVELS})'
    )
    op.execute(
        'DELETE FROM tutor_posts WHERE NOT EXISTS ('
        'SELECT 1 FROM tutor_post_class_levels '
        'WHERE tutor_post_class_levels.tutor_post_id = tutor_posts.id)'
    )
    op.execute("DELETE FROM class_levels WHERE level = 'higher_education'")

    op.execute('ALTER TYPE education_level RENAME TO education_level_old')
    op.execute(
        "CREATE TYPE education_level AS ENUM "
        "('preschool', 'elementary', 'intermediate', 'secondary')"
    )
    op.execute(
        'ALTER TABLE class_levels ALTER COLUMN level TYPE education_level '
        'USING level::text::education_level'
    )
    op.execute('DROP TYPE education_level_old')


def downgrade() -> None:
    op.execute("ALTER TYPE education_level ADD VALUE IF NOT EXISTS 'higher_education'")

    op.drop_index(op.f('ix_tutor_profile_subjects_subject_id'), table_name='tutor_profile_subjects')
    op.drop_table('tutor_profile_subjects')
    op.drop_index(
        op.f('ix_tutor_profile_class_levels_class_level_id'),
        table_name='tutor_profile_class_levels',
    )
    op.drop_table('tutor_profile_class_levels')
