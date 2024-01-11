"""add content column to post table

Revision ID: 26163492ada6
Revises: d4fd1ec4157b
Create Date: 2024-01-08 11:52:39.192410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26163492ada6'
down_revision: Union[str, None] = 'd4fd1ec4157b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass