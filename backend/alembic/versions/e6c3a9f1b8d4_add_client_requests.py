"""add client requests

Revision ID: e6c3a9f1b8d4
Revises: d4f1b6a8c3e2
Create Date: 2026-10-13 12:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e6c3a9f1b8d4'
down_revision: Union[str, Sequence[str], None] = 'd4f1b6a8c3e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


request_status = sa.Enum(
    'pending', 'accepted', 'rejected', 'cancelled', name='request_status'
)


def upgrade() -> None:
    op.create_table(
        'client_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('tutor_post_id', sa.Integer(), nullable=False),
        sa.Column('status', request_status, server_default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['client_profiles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tutor_post_id'], ['tutor_posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_client_requests_id'), 'client_requests', ['id'], unique=False)
    op.create_index(op.f('ix_client_requests_client_id'), 'client_requests', ['client_id'], unique=False)
    op.create_index(op.f('ix_client_requests_tutor_post_id'), 'client_requests', ['tutor_post_id'], unique=False)
    op.create_index(op.f('ix_client_requests_status'), 'client_requests', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_client_requests_status'), table_name='client_requests')
    op.drop_index(op.f('ix_client_requests_tutor_post_id'), table_name='client_requests')
    op.drop_index(op.f('ix_client_requests_client_id'), table_name='client_requests')
    op.drop_index(op.f('ix_client_requests_id'), table_name='client_requests')
    op.drop_table('client_requests')
    request_status.drop(op.get_bind(), checkfirst=True)
