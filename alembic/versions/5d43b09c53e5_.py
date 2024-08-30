"""empty message

Revision ID: 5d43b09c53e5
Revises: 12d7c6a5d070
Create Date: 2024-08-29 22:57:22.839788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d43b09c53e5'
down_revision: Union[str, None] = '12d7c6a5d070'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Posts',sa.Column('content', sa.String(),nullable=False))


def downgrade():
    op.drop_column('Posts','content')
