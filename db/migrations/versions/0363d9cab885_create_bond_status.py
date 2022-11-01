"""create bond status

Revision ID: 0363d9cab885
Revises: 295b1d12b6dd
Create Date: 2022-10-31 20:26:33.478939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0363d9cab885'
down_revision = '295b1d12b6dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bonds', sa.Column('status', sa.Enum('posted', 'sold', name='bondstatus'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bonds', 'status')
    # ### end Alembic commands ###
