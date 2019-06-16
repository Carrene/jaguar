"""empty message

Revision ID: c0574d2ab64a
Revises: 4d7a03009718
Create Date: 2019-06-16 15:45:05.782902

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import orm

from jaguar.models import Member


# revision identifiers, used by Alembic.
revision = 'c0574d2ab64a'
down_revision = '4d7a03009718'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.add_column(
        'member',
        sa.Column('name', sa.Unicode(length=20), nullable=True)
    )

    members = session.query(Member).all()
    for member in members:
        member.name = member.title

    session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('member', 'name')
    # ### end Alembic commands ###
