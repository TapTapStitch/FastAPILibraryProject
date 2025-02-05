"""Initial migration

Revision ID: e9635d85c109
Revises: 
Create Date: 2024-12-31 10:35:00.887175

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e9635d85c109"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("year_of_publication", sa.Integer(), nullable=True),
        sa.Column("isbn", sa.String(), nullable=True),
        sa.Column("series", sa.String(), nullable=True),
        sa.Column("file_link", sa.String(), nullable=True),
        sa.Column("edition", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("isbn"),
    )
    op.create_index(op.f("ix_books_id"), "books", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_books_id"), table_name="books")
    op.drop_table("books")
    # ### end Alembic commands ###
