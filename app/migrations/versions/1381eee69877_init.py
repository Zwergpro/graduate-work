"""init

Revision ID: 1381eee69877
Revises: 
Create Date: 2021-04-29 18:00:45.370884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1381eee69877'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dataset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('dt_start', sa.DateTime(), nullable=True),
    sa.Column('dt_end', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('start', 'end', name='datasetstatus'), nullable=True),
    sa.Column('type', sa.Enum('top_one', 'appt_docs', name='datasettype'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dataset')
    # ### end Alembic commands ###
