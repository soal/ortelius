"""empty message

Revision ID: 07876c46d2ec
Revises: None
Create Date: 2016-05-06 09:27:09.797893

"""

# revision identifiers, used by Alembic.
revision = '07876c46d2ec'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_coordinates_quadrant_hash'), 'coordinates', ['quadrant_hash'], unique=False)
    op.create_index(op.f('ix_fact_weight'), 'fact', ['weight'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_fact_weight'), table_name='fact')
    op.drop_index(op.f('ix_coordinates_quadrant_hash'), table_name='coordinates')
    ### end Alembic commands ###
