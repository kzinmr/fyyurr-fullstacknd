"""empty message

Revision ID: 2827d894735e
Revises: badc9aba148c
Create Date: 2019-09-30 14:45:42.264321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2827d894735e"
down_revision = "badc9aba148c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "Artist", "image_link", existing_type=sa.VARCHAR(length=500), nullable=True
    )
    op.alter_column(
        "Artist", "phone", existing_type=sa.VARCHAR(length=120), nullable=True
    )
    op.alter_column(
        "Venue", "image_link", existing_type=sa.VARCHAR(length=500), nullable=True
    )
    op.alter_column(
        "Venue", "phone", existing_type=sa.VARCHAR(length=120), nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "Venue", "phone", existing_type=sa.VARCHAR(length=120), nullable=False
    )
    op.alter_column(
        "Venue", "image_link", existing_type=sa.VARCHAR(length=500), nullable=False
    )
    op.alter_column(
        "Artist", "phone", existing_type=sa.VARCHAR(length=120), nullable=False
    )
    op.alter_column(
        "Artist", "image_link", existing_type=sa.VARCHAR(length=500), nullable=False
    )
    # ### end Alembic commands ###
