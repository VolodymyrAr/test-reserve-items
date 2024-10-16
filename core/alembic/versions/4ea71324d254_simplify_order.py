"""simplify_order

Revision ID: 4ea71324d254
Revises: a73bc4b83cf7
Create Date: 2024-10-15 22:08:45.706742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ea71324d254'
down_revision: Union[str, None] = 'a73bc4b83cf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_order_item_id', table_name='order_item')
    op.drop_index('ix_order_item_quantity', table_name='order_item')
    op.drop_table('order_item')
    op.add_column('order', sa.Column('item_id', sa.Integer(), nullable=False))
    op.add_column('order', sa.Column('quantity', sa.Integer(), nullable=False))
    op.add_column('order', sa.Column('price', sa.Integer(), nullable=False))
    op.add_column('order', sa.Column('discount', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_order_quantity'), 'order', ['quantity'], unique=False)
    op.create_foreign_key(None, 'order', 'item', ['item_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_index(op.f('ix_order_quantity'), table_name='order')
    op.drop_column('order', 'discount')
    op.drop_column('order', 'price')
    op.drop_column('order', 'quantity')
    op.drop_column('order', 'item_id')
    op.create_table('order_item',
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('discount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], name='order_item_item_id_fkey'),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], name='order_item_order_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='order_item_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='order_item_pkey')
    )
    op.create_index('ix_order_item_quantity', 'order_item', ['quantity'], unique=False)
    op.create_index('ix_order_item_id', 'order_item', ['id'], unique=False)
    # ### end Alembic commands ###
