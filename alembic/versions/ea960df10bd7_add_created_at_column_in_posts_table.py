"""add created at column in posts table'

Revision ID: ea960df10bd7
Revises: fe07baf03835
Create Date: 2024-08-30 17:10:40.288675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea960df10bd7'
down_revision: Union[str, None] = 'fe07baf03835'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                    server_default=sa.text('now()'),nullable=False))


def downgrade():
    op.drop_column('Posts','created_at')
