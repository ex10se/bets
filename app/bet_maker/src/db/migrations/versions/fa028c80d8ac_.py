"""empty message

Revision ID: fa028c80d8ac
Revises: 
Create Date: 2023-04-22 10:34:48.636623

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'fa028c80d8ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=False, comment='Имя'),
    sa.Column('amount', sa.Numeric(precision=20, scale=2), nullable=True, comment='Сумма денег на счету'),
    sa.Column('auth_key', sa.Uuid(), nullable=True, comment='Ключ авторизации'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('coefficient', sa.Numeric(precision=5, scale=2), nullable=False, comment='Коэффициент на победу'),
    sa.Column('deadline', sa.TIMESTAMP(), nullable=False, comment='Время окончания приёма ставок (UTC)'),
    sa.Column('state', sa.Enum('unknown', 'loose', 'win', name='eventstate', native_enum=False), nullable=False, comment='Состояние события относительно первой команды'),
    sa.CheckConstraint('coefficient > 0'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bet',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('state', sa.Enum('unknown', 'lost', 'earned', name='betstate', native_enum=False), nullable=True, comment='Результат ставки'),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.Column('bet_amount', sa.Numeric(precision=20, scale=2), nullable=False, comment='Поставленная сумма денег'),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('date_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bet')
    op.drop_table('event')
    op.drop_table('client')
    # ### end Alembic commands ###
