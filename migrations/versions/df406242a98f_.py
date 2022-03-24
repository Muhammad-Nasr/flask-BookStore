"""empty message

Revision ID: df406242a98f
Revises: 673b0ff2b530
Create Date: 2022-03-24 03:18:34.905481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df406242a98f'
down_revision = '673b0ff2b530'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_book_author'), 'book', ['author'], unique=False)
    op.create_index(op.f('ix_book_date_added'), 'book', ['date_added'], unique=False)
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    op.create_unique_constraint(None, 'book', ['book_id'])
    op.alter_column('reader', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reader', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.drop_constraint(None, 'book', type_='unique')
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.drop_index(op.f('ix_book_date_added'), table_name='book')
    op.drop_index(op.f('ix_book_author'), table_name='book')
    # ### end Alembic commands ###
