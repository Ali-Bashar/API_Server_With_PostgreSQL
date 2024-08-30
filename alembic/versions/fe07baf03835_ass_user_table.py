"""ass user table

Revision ID: fe07baf03835
Revises: 90f8b02b71b6
Create Date: 2024-08-29 23:28:03.783326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe07baf03835'
down_revision: Union[str, None] = '90f8b02b71b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('User',
                    sa.Column('user_id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('user_id'),
                    sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('User')
