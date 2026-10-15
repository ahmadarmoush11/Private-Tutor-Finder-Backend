"""add confirmed request status

Revision ID: f8b2d5e7a4c1
Revises: e6c3a9f1b8d4
Create Date: 2026-10-13 12:40:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'f8b2d5e7a4c1'
down_revision: Union[str, Sequence[str], None] = 'e6c3a9f1b8d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute(
            "ALTER TYPE request_status ADD VALUE IF NOT EXISTS 'confirmed' AFTER 'accepted'"
        )


def downgrade() -> None:
    op.execute("UPDATE client_requests SET status = 'accepted' WHERE status = 'confirmed'")
    op.execute("ALTER TYPE request_status RENAME TO request_status_old")
    op.execute(
        "CREATE TYPE request_status AS ENUM ('pending', 'accepted', 'rejected', 'cancelled')"
    )
    op.execute("ALTER TABLE client_requests ALTER COLUMN status DROP DEFAULT")
    op.execute(
        "ALTER TABLE client_requests ALTER COLUMN status TYPE request_status "
        "USING status::text::request_status"
    )
    op.execute("ALTER TABLE client_requests ALTER COLUMN status SET DEFAULT 'pending'")
    op.execute("DROP TYPE request_status_old")
