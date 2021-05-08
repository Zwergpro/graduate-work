"""add new DatasetStatus

Revision ID: 92d11f8ca30f
Revises: 1381eee69877
Create Date: 2021-05-05 23:21:46.305998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92d11f8ca30f'
down_revision = '1381eee69877'
branch_labels = None
depends_on = None


old_type = sa.Enum('start', 'end', name='datasetstatus')
new_type = sa.Enum('start', 'end', 'fail', name='datasetstatus')
tmp_type = sa.Enum('start', 'end', 'fail', name='_datasetstatus')


def upgrade():
    # Create a tempoary "_status" type, convert and drop the "old" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE dataset ALTER COLUMN status TYPE _datasetstatus USING status::text::_datasetstatus')
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" status type
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE dataset ALTER COLUMN status TYPE datasetstatus USING status::text::datasetstatus')
    tmp_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    op.execute("UPDATE dataset SET status = 'end' where status = 'fail'")
    # Create a tempoary "_status" type, convert and drop the "new" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE dataset ALTER COLUMN status TYPE _datasetstatus USING status::text::_datasetstatus')
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" status type
    old_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE dataset ALTER COLUMN status TYPE datasetstatus USING status::text::datasetstatus')
    tmp_type.drop(op.get_bind(), checkfirst=False)
