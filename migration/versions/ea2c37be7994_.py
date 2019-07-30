"""Add first name and last name to member model

Revision ID: ea2c37be7994
Revises: c0574d2ab64a
Create Date: 2019-07-30 12:27:51.129847

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

from jaguar.models import Member


# revision identifiers, used by Alembic.
revision = 'ea2c37be7994'
down_revision = 'c0574d2ab64a'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.execute('alter table member rename name to first_name;')
    op.add_column(
        'member',
        sa.Column('last_name', sa.Unicode(length=20), nullable=True)
    )
    for member in session.query(Member):
        member.last_name = ''

    session.commit()

    op.execute('ALTER TABLE member ALTER last_name SET NOT NULL;')

def downgrade():
    op.execute('alter table member rename first_name to name;')
    op.drop_column('member', 'last_name')

