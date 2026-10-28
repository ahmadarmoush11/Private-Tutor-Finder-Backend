"""add reviewed_by_id to degree verifications

Revision ID: c5e1a7b3d9f4
Revises: b3d9f5a1c7e2
Create Date: 2026-10-28 12:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c5e1a7b3d9f4'
down_revision: Union[str, Sequence[str], None] = 'b3d9f5a1c7e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('degree_verifications', sa.Column('reviewed_by_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'degree_verifications_reviewed_by_id_fkey',
        'degree_verifications',
        'users',
        ['reviewed_by_id'],
        ['id'],
        ondelete='SET NULL',
    )
    op.create_index(
        op.f('ix_degree_verifications_reviewed_by_id'),
        'degree_verifications',
        ['reviewed_by_id'],
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_degree_verifications_reviewed_by_id'), table_name='degree_verifications')
    op.drop_constraint(
        'degree_verifications_reviewed_by_id_fkey',
        'degree_verifications',
        type_='foreignkey',
    )
    op.drop_column('degree_verifications', 'reviewed_by_id')
