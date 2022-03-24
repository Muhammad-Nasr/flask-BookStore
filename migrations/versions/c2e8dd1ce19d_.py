"""empty message

Revision ID: c2e8dd1ce19d
Revises: 525935687efd
Create Date: 2022-03-23 14:13:39.269272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2e8dd1ce19d'
down_revision = '525935687efd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('book_book_id_key', 'book', type_='unique')
    op.drop_index('ix_book_title', table_name='book')
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    op.alter_column('reader', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reader', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.create_index('ix_book_title', 'book', ['title'], unique=False)
    op.create_unique_constraint('book_book_id_key', 'book', ['book_id'])
    # ### end Alembic commands ###
