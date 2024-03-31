"""empty message

Revision ID: 63e9b2b07c6b
Revises: 84201252c013
Create Date: 2024-03-30 22:04:27.908940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63e9b2b07c6b'
down_revision = '84201252c013'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coupon', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Float(precision=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coupon', schema=None) as batch_op:
        batch_op.drop_column('price')

    # ### end Alembic commands ###
