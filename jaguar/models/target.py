from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin,relationship
from restfulpy.taskqueue import Task
from restfulpy.logging_ import get_logger
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table

from jaguar.models.user import User


room_member_table = Table(
    'room_member',
    DeclarativeBase.metadata,
    Field('room_id', Integer, ForeignKey('room.id')),
    Field('member_id', Integer, ForeignKey('user.id'))
)

class Target(DeclarativeBase, ModifiedMixin):
    __tablename__  = 'target'

    id = Field(Integer, primary_key=True)

    title = Field(
        Unicode(50),
        nullable = True,
        json = 'title'
    )
    type = Field(
        Unicode(25)
    )

    __mapper_args__ = {
        'polymorphic_identity' :__tablename__,
        'polymorphic_on' : type,
    }


class Room(Target):
    __tablename__ = 'room'

    id = Field (
        Integer,
        ForeignKey('target.id'),
        primary_key = True,
        json = 'target_id'
    )

    member = relationship(
        "User",
        secondary=room_member_table,
        protected=True
    )

    __mapper_args__ = {
        'polymorphic_identity' : __tablename__,
    }


class Direct(Target):
    __tablename__ = 'direct'

    id = Field (
        Integer,
        ForeignKey('target.id'),
        primary_key = True,
        json = 'target_id'
    )

    __mapper_args__ = {
        'polymorphic_identity' : __tablename__,
    }

