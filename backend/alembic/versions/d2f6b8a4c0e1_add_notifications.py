"""add notifications

Revision ID: d2f6b8a4c0e1
Revises: c9e5a1f7b3d2
Create Date: 2026-10-23 15:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd2f6b8a4c0e1'
down_revision: Union[str, Sequence[str], None] = 'c9e5a1f7b3d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


notification_type = sa.Enum(
    'tutor_available',
    'lesson_request_received',
    'lesson_request_accepted',
    'lesson_request_rejected',
    'lesson_request_confirmed',
    name='notification_type',
)


def upgrade() -> None:
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipient_id', sa.Integer(), nullable=False),
        sa.Column('actor_id', sa.Integer(), nullable=True),
        sa.Column('type', notification_type, nullable=False),
        sa.Column('lesson_request_id', sa.Integer(), nullable=True),
        sa.Column('client_post_id', sa.Integer(), nullable=True),
        sa.Column('is_read', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['actor_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['lesson_request_id'], ['lesson_requests.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['client_post_id'], ['client_posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'])
    op.create_index(op.f('ix_notifications_actor_id'), 'notifications', ['actor_id'])
    op.create_index(op.f('ix_notifications_lesson_request_id'), 'notifications', ['lesson_request_id'])
    op.create_index(op.f('ix_notifications_client_post_id'), 'notifications', ['client_post_id'])
    op.create_index(
        'ix_notifications_recipient_id_created_at',
        'notifications',
        ['recipient_id', 'created_at'],
    )
    op.create_index(
        'ix_notifications_recipient_id_unread',
        'notifications',
        ['recipient_id'],
        postgresql_where=sa.text('is_read = false'),
    )


def downgrade() -> None:
    op.drop_index('ix_notifications_recipient_id_unread', table_name='notifications')
    op.drop_index('ix_notifications_recipient_id_created_at', table_name='notifications')
    op.drop_index(op.f('ix_notifications_client_post_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_lesson_request_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_actor_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.drop_table('notifications')
    notification_type.drop(op.get_bind(), checkfirst=True)
