"""update dataset depth

Revision ID: 327cd266f7b3
Revises: 26934c96ec80
Create Date: 2021-09-28 19:58:31.618442

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "327cd266f7b3"
down_revision = "26934c96ec80"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("datasets", sa.Column("collections", sa.JSON(), nullable=True))
    op.drop_column("datasets", "location")
    op.drop_column("datasets", "fields")
    op.drop_column("datasets", "dataset_type")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "datasets",
        sa.Column("dataset_type", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "datasets",
        sa.Column(
            "fields",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "datasets",
        sa.Column("location", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("datasets", "collections")
    # ### end Alembic commands ###
