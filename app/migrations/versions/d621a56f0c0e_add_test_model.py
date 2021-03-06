"""add test model

Revision ID: d621a56f0c0e
Revises: 3758f411470a
Create Date: 2021-05-16 15:27:23.501016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd621a56f0c0e'
down_revision = '3758f411470a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('dt_start', sa.DateTime(), nullable=True),
    sa.Column('dt_end', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('start', 'end', 'fail', name='teststatus'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    # ### end Alembic commands ###
