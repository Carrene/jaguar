
from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin, \
    relationship, OrderingMixin, FilteringMixin, PaginationMixin
from restfulpy.taskqueue import RestfulpyTask
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table, \
    UniqueConstraint

from .membership import User
from .envelop import Envelop


#target_member = Table(
#    'target_member',
#    DeclarativeBase.metadata,
#    Field('target_id', Integer, ForeignKey('target.id')),
#    Field('member_id', Integer, ForeignKey('user.id'))
#)
class TargetMember(DeclarativeBase):
    __tablename__ = 'target_member'

    target_id = Field(Integer, ForeignKey('target.id'), primary_key=True)
    member_id = Field(Integer, ForeignKey('user.id'), primary_key=True)


room_administrator = Table(
    'room_administrator',
    DeclarativeBase.metadata,
    Field('room_id', Integer, ForeignKey('target.id')),
    Field('member_id', Integer, ForeignKey('user.id'))
)


class Target(ModifiedMixin, OrderingMixin, FilteringMixin, PaginationMixin,
             DeclarativeBase):
    __tablename__ = 'target'

    id = Field(Integer, primary_key=True)
    title = Field(
        Unicode(50),
        nullable=True,
        json='title'
    )
    type = Field(Unicode(25))

    # since the number of collections are small, the selectin strategy is
    # more efficient for loading
    members = relationship(
        'User',
        secondary='target_member',
        backref='rooms',
        lazy='selectin',
    )
    envelop_id = relationship('Envelop')
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type,
    }


class Room(Target):

    owner_id = Field(Integer, ForeignKey('user.id'), nullable=True)
    owner = relationship('User', back_populates='room')

    # since the number of collections are small, the selectin strategy is
    # more efficient for loading
    administrators = relationship(
        'User',
        secondary=room_administrator,
        backref='administrator_of',
        protected=True,
        lazy='selectin'
    )
    UniqueConstraint(owner_id, Target.title, name='unique_room')

    def to_dict(self):
        member_ids = [member.id for member in self.members]
        administrator_ids =\
            [administrator.id for administrator in self.administrators]
        return dict(
            id=self.id,
            title=self.title,
            type=self.type,
            memberIds=member_ids,
            administratorIds=administrator_ids,
            ownerId=self.owner_id
        )
    messages = relationship('Envelop')
    __mapper_args__ = {
        'polymorphic_identity': 'room',
    }


class Direct(Target):

    __mapper_args__ = {
        'polymorphic_identity': 'direct',
    }

