"""empty message

Revision ID: 400d246181f6
Revises: 
Create Date: 2024-04-11 10:51:53.695192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '400d246181f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('spotify_username', sa.String(length=64), nullable=True),
    sa.Column('bio', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_spotify_username'), ['spotify_username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_spotify_username'))

    op.drop_table('users')
    # ### end Alembic commands ###
