from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin,relationship
from restfulpy.taskqueue import Task
from restfulpy.logging_ import get_logger
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table

from .membership import User
from .envelop import Envelop


room_member_table = Table(
    'room_member',
    DeclarativeBase.metadata,
    Field('room_id', Integer, ForeignKey('room.id')),
    Field('member_id', Integer, ForeignKey('user.id'))
)
room_administrator_table = Table(
    'room_administrator',
    DeclarativeBase.metadata,
    Field('room_id', Integer, ForeignKey('room.id')),
    Field('member_id', Integer, ForeignKey('user.id'))
)


class Target(DeclarativeBase, ModifiedMixin):
    __tablename__  = 'target'

    id = Field(Integer, primary_key=True)

    title = Field(
        Unicode(50),
        nullable=True,
        json='title'
    )
    type = Field(
        Unicode(25)
    )
    envelop_id = relationship('Envelop')

    __mapper_args__ = {
        'polymorphic_identity' :__tablename__,
        'polymorphic_on' : type,
    }


class Room(Target):
    __tablename__ = 'room'

    id = Field (
        Integer,
        ForeignKey('target.id'),
        primary_key=True,
        json='target_id'
    )

    # since the number of collections are small, the selectin strategy is
    # more efficient for loading
    members = relationship(
        "User",
        secondary=room_member_table,
        backref='rooms',
        protected=True,
        lazy='selectin'
    )

    # since the number of collections are small, the selectin strategy is
    # more efficient for loading
    administrators = relationship(
        "User",
        secondary=room_administrator_table,
        backref='administrator_of',
        protected=True,
        lazy='selectin'
    )

    __mapper_args__ = {
        'polymorphic_identity' : __tablename__,
    }


class Direct(Target):
    __tablename__ = 'direct'

    id = Field (
        Integer,
        ForeignKey('target.id'),
        primary_key=True,
        json='target_id'
    )

    __mapper_args__ = {
        'polymorphic_identity' : __tablename__,
    }

