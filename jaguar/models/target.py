
from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin, \
    relationship, OrderingMixin, FilteringMixin, PaginationMixin
from restfulpy.taskqueue import RestfulpyTask
from restfulpy.logging_ import get_logger
from restfulpy.orm import DBSession
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table

from .membership import User
from .envelop import Envelop


target_member = Table(
    'target_member',
    DeclarativeBase.metadata,
    Field('target_id', Integer, ForeignKey('target.id')),
    Field('member_id', Integer, ForeignKey('user.id'))
)

room_administrator = Table(
    'room_administrator',
    DeclarativeBase.metadata,
    Field('room_id', Integer, ForeignKey('room.id')),
    Field('member_id', Integer, ForeignKey('user.id'))
)


class Target(
    DeclarativeBase,
    ModifiedMixin,
    OrderingMixin,
    FilteringMixin,
    PaginationMixin
):
    __tablename__ = 'target'

    id = Field(Integer, primary_key=True)
    title = Field(
        Unicode(50),
        nullable=True,
        json='title'
    )
    type = Field(
        Unicode(25)
    )
    # since the number of collections are small, the selectin strategy is
    # more efficient for loading
    members = relationship(
        'User',
        secondary=target_member,
        backref='rooms',
        protected=True,
        lazy='selectin'
    )
    envelop_id = relationship('Envelop')
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type,
    }


class Room(Target):
    __tablename__ = 'room'

    id = Field(
        Integer,
        ForeignKey('target.id'),
        primary_key=True,
        json='room_id',
    )
    # since the number of collections are small, the selectin strategy is
    # more efficient for loading
    administrators = relationship(
        'User',
        secondary=room_administrator,
        backref='administrator_of',
        protected=True,
        lazy='selectin'
    )
    owner_id = Field(Integer, ForeignKey('user.id'), nullable=True)

    def to_dict(self):
        member_ids = [member.id for member in self.members]
        administrator_ids =\
            [administrator.id for administrator in self.administrators]
        return dict(
            id=self.id,
            title=self.title,
            type=self.type,
            member_ids=member_ids,
            administrator_ids = administrator_ids,
            owner_id = self.owner_id
        )
    messages = relationship('Envelop')
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Direct(Target):
    __tablename__ = 'direct'

    id = Field(
        Integer,
        ForeignKey('target.id'),
        primary_key=True,
        json='target_id'
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

