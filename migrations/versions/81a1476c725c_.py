"""empty message

Revision ID: 81a1476c725c
Revises: 3e9eedd78226
Create Date: 2025-01-19 13:22:07.091728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81a1476c725c'
down_revision = '3e9eedd78226'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurant_pizza',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('pizza_id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pizza_id'], ['pizzas.id'], name=op.f('fk_restaurant_pizza_pizza_id_pizzas')),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], name=op.f('fk_restaurant_pizza_restaurant_id_restaurant')),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('restaurant_pizzas')
    op.drop_table('restaurants')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurants',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('address', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurant_pizzas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('pizza_id', sa.INTEGER(), nullable=False),
    sa.Column('restaurant_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['pizza_id'], ['pizzas.id'], name='fk_restaurant_pizzas_pizza_id_pizzas'),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], name='fk_restaurant_pizzas_restaurant_id_restaurants'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('restaurant_pizza')
    op.drop_table('restaurant')
    # ### end Alembic commands ###
