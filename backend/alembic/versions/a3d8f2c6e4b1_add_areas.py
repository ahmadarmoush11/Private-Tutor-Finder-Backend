"""add areas; link posts and tutor profiles to areas; remove location and address

Revision ID: a3d8f2c6e4b1
Revises: f1c7e3a9b5d2
Create Date: 2026-10-29 12:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a3d8f2c6e4b1'
down_revision: Union[str, Sequence[str], None] = 'f1c7e3a9b5d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


AREA_TABLES = ['client_posts', 'tutor_posts', 'tutor_profiles']
POST_TABLES = ['client_posts', 'tutor_posts']


def upgrade() -> None:
    op.create_table(
        'areas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('district', sa.String(length=100), nullable=False),
        sa.Column('governorate', sa.String(length=100), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'district', name='uq_areas_name_district'),
    )
    op.create_index(op.f('ix_areas_id'), 'areas', ['id'])
    op.create_index(op.f('ix_areas_district'), 'areas', ['district'])
    op.create_index(op.f('ix_areas_governorate'), 'areas', ['governorate'])

    for table in AREA_TABLES:
        op.add_column(table, sa.Column('area_id', sa.Integer(), nullable=True))
        op.create_foreign_key(
            f'{table}_area_id_fkey', table, 'areas', ['area_id'], ['id'], ondelete='RESTRICT'
        )
        op.create_index(op.f(f'ix_{table}_area_id'), table, ['area_id'])

    for table in POST_TABLES:
        op.drop_column(table, 'location')
        op.drop_column(table, 'address_details')


def downgrade() -> None:
    for table in POST_TABLES:
        op.add_column(
            table,
            sa.Column('address_details', sa.String(length=255), server_default='', nullable=False),
        )
        op.add_column(table, sa.Column('location', sa.String(length=150), nullable=True))

    for table in AREA_TABLES:
        op.drop_index(op.f(f'ix_{table}_area_id'), table_name=table)
        op.drop_constraint(f'{table}_area_id_fkey', table, type_='foreignkey')
        op.drop_column(table, 'area_id')

    op.drop_index(op.f('ix_areas_governorate'), table_name='areas')
    op.drop_index(op.f('ix_areas_district'), table_name='areas')
    op.drop_index(op.f('ix_areas_id'), table_name='areas')
    op.drop_table('areas')
