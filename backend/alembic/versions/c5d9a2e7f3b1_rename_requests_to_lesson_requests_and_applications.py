"""rename client requests to lesson requests and tutor requests to applications

Revision ID: c5d9a2e7f3b1
Revises: b4e8f1a6c9d3
Create Date: 2026-10-17 11:40:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'c5d9a2e7f3b1'
down_revision: Union[str, Sequence[str], None] = 'b4e8f1a6c9d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


RENAMES = [
    ('client_requests', 'lesson_requests', ['client_id', 'tutor_post_id']),
    ('tutor_requests', 'applications', ['tutor_id', 'client_post_id']),
]


def _rename(old: str, new: str, foreign_keys: list[str]) -> None:
    op.rename_table(old, new)
    op.execute(f'ALTER SEQUENCE {old}_id_seq RENAME TO {new}_id_seq')
    op.execute(f'ALTER TABLE {new} RENAME CONSTRAINT {old}_pkey TO {new}_pkey')
    for column in foreign_keys:
        op.execute(
            f'ALTER TABLE {new} RENAME CONSTRAINT {old}_{column}_fkey TO {new}_{column}_fkey'
        )
    for column in ['id', 'status', *foreign_keys]:
        op.execute(f'ALTER INDEX ix_{old}_{column} RENAME TO ix_{new}_{column}')


def upgrade() -> None:
    for old, new, foreign_keys in RENAMES:
        _rename(old, new, foreign_keys)


def downgrade() -> None:
    for old, new, foreign_keys in RENAMES:
        _rename(new, old, foreign_keys)
