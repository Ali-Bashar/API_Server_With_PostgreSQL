"""create posts table

Revision ID: 12d7c6a5d070
Revises: 
Create Date: 2024-08-29 22:30:15.390855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12d7c6a5d070'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('Posts',sa.Column('post_id',sa.Integer(),nullable=False,
        primary_key=True),sa.Column('title',sa.String(),nullable=False))


def downgrade():
    op.drop_table('Posts')
