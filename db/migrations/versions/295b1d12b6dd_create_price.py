"""Create price

Revision ID: 295b1d12b6dd
Revises: 24ad94b182de
Create Date: 2022-10-28 04:42:57.881949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "295b1d12b6dd"
down_revision = "24ad94b182de"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "bonds", sa.Column("price", sa.DECIMAL(precision=13, scale=4), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("bonds", "price")
    # ### end Alembic commands ###
