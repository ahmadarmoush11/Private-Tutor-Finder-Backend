"""add budget to client posts and tutor requests

Revision ID: b4e8f1a6c9d3
Revises: a9d3e7c5f2b8
Create Date: 2026-10-16 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'b4e8f1a6c9d3'
down_revision: Union[str, Sequence[str], None] = 'a9d3e7c5f2b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


currency = postgresql.ENUM('USD', 'LBP', name='currency', create_type=False)
price_unit = postgresql.ENUM(
    'hour', 'session', 'week', 'month', name='price_unit', create_type=False
)
request_status = postgresql.ENUM(
    'pending', 'accepted', 'confirmed', 'rejected', 'cancelled',
    name='request_status',
    create_type=False,
)


def upgrade() -> None:
    op.add_column('client_posts', sa.Column('budget_min', sa.Numeric(12, 2), nullable=True))
    op.add_column('client_posts', sa.Column('budget_max', sa.Numeric(12, 2), nullable=True))
    op.add_column('client_posts', sa.Column('currency', currency, nullable=True))
    op.add_column('client_posts', sa.Column('price_unit', price_unit, nullable=True))

    op.create_table(
        'tutor_requests',
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
    op.create_index(op.f('ix_tutor_requests_id'), 'tutor_requests', ['id'], unique=False)
    op.create_index(op.f('ix_tutor_requests_tutor_id'), 'tutor_requests', ['tutor_id'], unique=False)
    op.create_index(op.f('ix_tutor_requests_client_post_id'), 'tutor_requests', ['client_post_id'], unique=False)
    op.create_index(op.f('ix_tutor_requests_status'), 'tutor_requests', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_tutor_requests_status'), table_name='tutor_requests')
    op.drop_index(op.f('ix_tutor_requests_client_post_id'), table_name='tutor_requests')
    op.drop_index(op.f('ix_tutor_requests_tutor_id'), table_name='tutor_requests')
    op.drop_index(op.f('ix_tutor_requests_id'), table_name='tutor_requests')
    op.drop_table('tutor_requests')

    op.drop_column('client_posts', 'price_unit')
    op.drop_column('client_posts', 'currency')
    op.drop_column('client_posts', 'budget_max')
    op.drop_column('client_posts', 'budget_min')
