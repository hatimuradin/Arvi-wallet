"""Initial migration

Revision ID: 221fad757a2d
Revises: 
Create Date: 2024-02-08 10:24:40.939253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '221fad757a2d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chargecode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_used', sa.Boolean(), nullable=False),
    sa.Column('used_at', sa.DateTime(), nullable=True),
    sa.Column('is_applied', sa.Boolean(), nullable=False),
    sa.Column('applied_at', sa.DateTime(), nullable=True),
    sa.Column('user_phone', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chargecode_id'), 'chargecode', ['id'], unique=False)
    op.create_table('discountcode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_used', sa.Boolean(), nullable=False),
    sa.Column('used_at', sa.DateTime(), nullable=True),
    sa.Column('is_applied', sa.Boolean(), nullable=False),
    sa.Column('applied_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_discountcode_id'), 'discountcode', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_discountcode_id'), table_name='discountcode')
    op.drop_table('discountcode')
    op.drop_index(op.f('ix_chargecode_id'), table_name='chargecode')
    op.drop_table('chargecode')
    # ### end Alembic commands ###
