"""replace is_verified with status on degree verifications

Revision ID: a1c7e3f9b5d8
Revises: f7b1d5a3e9c2
Create Date: 2026-10-28 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1c7e3f9b5d8'
down_revision: Union[str, Sequence[str], None] = 'f7b1d5a3e9c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


verification_status = sa.Enum('pending', 'verified', 'rejected', name='verification_status')


def upgrade() -> None:
    verification_status.create(op.get_bind(), checkfirst=True)
    op.add_column(
        'degree_verifications',
        sa.Column('status', verification_status, server_default='pending', nullable=False),
    )
    op.execute("UPDATE degree_verifications SET status = 'verified' WHERE is_verified")
    op.drop_column('degree_verifications', 'is_verified')
    op.create_index(
        op.f('ix_degree_verifications_status'),
        'degree_verifications',
        ['status'],
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_degree_verifications_status'), table_name='degree_verifications')
    op.add_column(
        'degree_verifications',
        sa.Column('is_verified', sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.execute("UPDATE degree_verifications SET is_verified = true WHERE status = 'verified'")
    op.drop_column('degree_verifications', 'status')
    verification_status.drop(op.get_bind(), checkfirst=True)
