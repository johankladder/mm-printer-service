"""create printers table

Revision ID: c13b397a1a90
Revises: 
Create Date: 2023-04-04 16:07:13.396346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c13b397a1a90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'printers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('readable_name', sa.String(50), nullable=False),
        sa.Column('progressor_identifier', sa.String(50), nullable=False),
        sa.Column('remote_identifier', sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('printers')
