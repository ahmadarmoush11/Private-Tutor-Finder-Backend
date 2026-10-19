"""replace applications with post availabilities

Revision ID: f4b8d2e6a1c3
Revises: e3a7c1d5b9f2
Create Date: 2026-10-19 12:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'f4b8d2e6a1c3'
down_revision: Union[str, Sequence[str], None] = 'e3a7c1d5b9f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


request_status = postgresql.ENUM(
    'pending', 'accepted', 'confirmed', 'rejected', 'cancelled',
    name='request_status',
    create_type=False,
)


def upgrade() -> None:
    op.drop_table('applications')

    op.create_table(
        'post_availabilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tutor_id', sa.Integer(), nullable=False),
        sa.Column('client_post_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutor_profiles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['client_post_id'], ['client_posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'tutor_id',
            'client_post_id',
            name='uq_post_availabilities_tutor_id_client_post_id',
        ),
    )
    op.create_index(op.f('ix_post_availabilities_id'), 'post_availabilities', ['id'])
    op.create_index(op.f('ix_post_availabilities_tutor_id'), 'post_availabilities', ['tutor_id'])
    op.create_index(
        op.f('ix_post_availabilities_client_post_id'),
        'post_availabilities',
        ['client_post_id'],
    )


def downgrade() -> None:
    op.drop_table('post_availabilities')

    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tutor_id', sa.Integer(), nullable=False),
        sa.Column('client_post_id', sa.Integer(), nullable=False),
        sa.Column('status', request_status, server_default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutor_profiles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['client_post_id'], ['client_posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_applications_id'), 'applications', ['id'])
    op.create_index(op.f('ix_applications_tutor_id'), 'applications', ['tutor_id'])
    op.create_index(op.f('ix_applications_client_post_id'), 'applications', ['client_post_id'])
    op.create_index(op.f('ix_applications_status'), 'applications', ['status'])
