"""empty message

Revision ID: cbb1f95814ac
Revises: 4ccad0e66866
Create Date: 2024-10-05 03:12:10.369966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbb1f95814ac'
down_revision = '4ccad0e66866'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('people_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('favorite_character_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'people', ['people_id'], ['id'])
        batch_op.drop_column('character_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorite_character_id_fkey', 'people', ['character_id'], ['id'])
        batch_op.drop_column('people_id')

    # ### end Alembic commands ###
