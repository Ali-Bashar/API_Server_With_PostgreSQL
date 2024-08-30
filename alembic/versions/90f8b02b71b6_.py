"""empty message

Revision ID: 90f8b02b71b6
Revises: 5d43b09c53e5
Create Date: 2024-08-29 23:05:55.123453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90f8b02b71b6'
down_revision: Union[str, None] = '5d43b09c53e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Posts',sa.Column('published',sa.Boolean(),
                                    server_default=sa.text("True"),nullable=False))
    

def downgrade() -> None:
    op.drop_column('Posts','published')
