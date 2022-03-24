"""empty message

Revision ID: 4452d811df3a
Revises: af7c45bc3b38
Create Date: 2022-03-22 21:23:17.691649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4452d811df3a'
down_revision = 'af7c45bc3b38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_reader_email', table_name='reader')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_reader_email', 'reader', ['email'], unique=False)
    # ### end Alembic commands ###
