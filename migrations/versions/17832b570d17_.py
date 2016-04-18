"""empty message

Revision ID: 17832b570d17
Revises: None
Create Date: 2016-04-18 09:46:28.602547

"""

# revision identifiers, used by Alembic.
revision = '17832b570d17'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coordinates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('long', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shape',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shapes_coordinates',
    sa.Column('shape_id', sa.Integer(), nullable=True),
    sa.Column('coordinates_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['coordinates_id'], ['coordinates.id'], ),
    sa.ForeignKeyConstraint(['shape_id'], ['shape.id'], )
    )
    op.add_column('fact', sa.Column('shape', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'fact', 'shape', ['shape'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fact', type_='foreignkey')
    op.drop_column('fact', 'shape')
    op.drop_table('shapes_coordinates')
    op.drop_table('shape')
    op.drop_table('coordinates')
    ### end Alembic commands ###