"""add degree verifications, remove is_degree_verified from tutor profiles

Revision ID: f7b1d5a3e9c2
Revises: e5a9c3f1d7b4
Create Date: 2026-10-25 10:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f7b1d5a3e9c2'
down_revision: Union[str, Sequence[str], None] = 'e5a9c3f1d7b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _create_photo_table(name: str) -> None:
    op.create_table(
        name,
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('degree_verification_id', sa.Integer(), nullable=False),
        sa.Column('photo_path', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['degree_verification_id'],
            ['degree_verifications.id'],
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f(f'ix_{name}_id'), name, ['id'])
    op.create_index(op.f(f'ix_{name}_degree_verification_id'), name, ['degree_verification_id'])


def _drop_photo_table(name: str) -> None:
    op.drop_index(op.f(f'ix_{name}_degree_verification_id'), table_name=name)
    op.drop_index(op.f(f'ix_{name}_id'), table_name=name)
    op.drop_table(name)


def upgrade() -> None:
    op.drop_column('tutor_profiles', 'is_degree_verified')

    op.create_table(
        'degree_verifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tutor_profile_id', sa.Integer(), nullable=False),
        sa.Column('degree', sa.String(length=150), nullable=False),
        sa.Column('is_verified', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['tutor_profile_id'], ['tutor_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_degree_verifications_id'), 'degree_verifications', ['id'])
    op.create_index(
        op.f('ix_degree_verifications_tutor_profile_id'),
        'degree_verifications',
        ['tutor_profile_id'],
    )

    _create_photo_table('degree_photos')
    _create_photo_table('national_id_photos')


def downgrade() -> None:
    _drop_photo_table('national_id_photos')
    _drop_photo_table('degree_photos')

    op.drop_index(op.f('ix_degree_verifications_tutor_profile_id'), table_name='degree_verifications')
    op.drop_index(op.f('ix_degree_verifications_id'), table_name='degree_verifications')
    op.drop_table('degree_verifications')

    op.add_column(
        'tutor_profiles',
        sa.Column('is_degree_verified', sa.Boolean(), server_default=sa.false(), nullable=False),
    )
