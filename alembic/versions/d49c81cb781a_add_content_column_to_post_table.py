"""add content column to post table

Revision ID: d49c81cb781a
Revises: 92173ba9f299
Create Date: 2024-01-08 10:25:05.456437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd49c81cb781a'
down_revision: Union[str, None] = '92173ba9f299'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
