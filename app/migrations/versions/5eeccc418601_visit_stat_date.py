"""visit_stat_date

Revision ID: 5eeccc418601
Revises: 307328fab28c
Create Date: 2023-06-26 16:08:28.357409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5eeccc418601'
down_revision = '307328fab28c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visit_stat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visit_stat', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
