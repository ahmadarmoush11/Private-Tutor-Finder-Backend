"""add reviewed_at to degree verifications

Revision ID: d7f3b9c5e1a6
Revises: c5e1a7b3d9f4
Create Date: 2026-10-28 12:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd7f3b9c5e1a6'
down_revision: Union[str, Sequence[str], None] = 'c5e1a7b3d9f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'degree_verifications',
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.execute(
        "UPDATE degree_verifications SET reviewed_at = updated_at "
        "WHERE reviewed_by_id IS NOT NULL OR status IN ('verified', 'rejected')"
    )


def downgrade() -> None:
    op.drop_column('degree_verifications', 'reviewed_at')
