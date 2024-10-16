"""fix price column

Revision ID: 11eef5c897e6
Revises: 4e22b4b97719
Create Date: 2024-10-10 17:44:18.848450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11eef5c897e6'
down_revision: Union[str, None] = '4e22b4b97719'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('item', 'price',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Integer(),
               existing_nullable=True,
                postgresql_using='price::integer')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('item', 'price',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###
