"""add_total_book_stat

Revision ID: 307328fab28c
Revises: aadb8a650083
Create Date: 2023-06-26 06:23:41.834845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '307328fab28c'
down_revision = 'aadb8a650083'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visit_number', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('visit_number')

    # ### end Alembic commands ###
