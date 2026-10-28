"""add cancelled to verification status

Revision ID: b3d9f5a1c7e2
Revises: a1c7e3f9b5d8
Create Date: 2026-10-28 11:05:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'b3d9f5a1c7e2'
down_revision: Union[str, Sequence[str], None] = 'a1c7e3f9b5d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE verification_status ADD VALUE IF NOT EXISTS 'cancelled'")


def downgrade() -> None:
    op.execute("UPDATE degree_verifications SET status = 'rejected' WHERE status = 'cancelled'")
    op.execute('ALTER TABLE degree_verifications ALTER COLUMN status DROP DEFAULT')
    op.execute('ALTER TYPE verification_status RENAME TO verification_status_old')
    op.execute("CREATE TYPE verification_status AS ENUM ('pending', 'verified', 'rejected')")
    op.execute(
        'ALTER TABLE degree_verifications ALTER COLUMN status TYPE verification_status '
        'USING status::text::verification_status'
    )
    op.execute("ALTER TABLE degree_verifications ALTER COLUMN status SET DEFAULT 'pending'")
    op.execute('DROP TYPE verification_status_old')
