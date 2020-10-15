"""Initial migration.

Revision ID: 8bbf67fdc451
Revises: 
Create Date: 2020-10-14 23:59:11.065139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bbf67fdc451'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('repository',
    sa.Column('name', sa.String(length=200), autoincrement=False, nullable=False),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.Column('access_type', sa.Boolean(), nullable=False),
    sa.Column('size', sa.String(length=100), nullable=False),
    sa.Column('stars', sa.String(length=100), nullable=False),
    sa.Column('watchers', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.String(length=100), nullable=False),
    sa.Column('updated_at', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('repository')
    op.drop_table('user')
    # ### end Alembic commands ###