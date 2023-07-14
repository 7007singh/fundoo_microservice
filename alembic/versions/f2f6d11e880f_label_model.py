"""label model

Revision ID: f2f6d11e880f
Revises: 637e090e0842
Create Date: 2023-07-12 16:03:50.781443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2f6d11e880f'
down_revision = '637e090e0842'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()





def upgrade_user_ms() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_user_ms() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_note_ms() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_note_ms() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_label_ms() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('label',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_label_id'), 'label', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade_label_ms() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_label_id'), table_name='label')
    op.drop_table('label')
    # ### end Alembic commands ###

