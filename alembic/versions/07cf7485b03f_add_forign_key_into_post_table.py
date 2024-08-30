"""add forign-key into post table

Revision ID: 07cf7485b03f
Revises: ea960df10bd7
Create Date: 2024-08-30 18:17:25.036575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07cf7485b03f'
down_revision: Union[str, None] = 'ea960df10bd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table="Posts",
                          referent_table="User",local_cols=['owner_id'],
                          remote_cols=['user_id'],ondelete='CASCADE')


def downgrade():
    op.drop_constraint('post_user_fk',table_name='Posts')
    op.drop_column('Posts','owner_id')