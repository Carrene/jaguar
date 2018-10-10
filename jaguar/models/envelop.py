
from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin,relationship,\
    ActivationMixin, OrderingMixin, FilteringMixin, PaginationMixin, \
    SoftDeleteMixin
from restfulpy.taskqueue import RestfulpyTask
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table, Boolean
from sqlalchemy.dialects.postgresql.json import JSONB

from .membership import Member


user_message = Table(
    'user_message',
    DeclarativeBase.metadata,
    Field('message_id', Integer, ForeignKey('envelop.id')),
    Field('user_id', Integer, ForeignKey('user.id')),
)


class Envelop(OrderingMixin, PaginationMixin, FilteringMixin, ActivationMixin,
              ModifiedMixin, SoftDeleteMixin, DeclarativeBase):
    __tablename__ = 'envelop'

    id = Field(Integer, primary_key=True)
    type = Field(Unicode(25))
    target_id = Field(Integer, ForeignKey('target.id'))
    sender_id = Field(Integer, ForeignKey('user.id'))
    body = Field(JSONB)
    __mapper_args__ = {
        'polymorphic_identity' :__tablename__,
        'polymorphic_on' : type,
    }


class Message(Envelop):

    mimetype=Field(Unicode(25))

    # Since collections would be fairly small,
    # selecin loding is chosen for this relationship.
    seen_by = relationship(
        'User',
        protected=False,
        secondary=user_message,
        lazy='selectin'
    )

    @property
    def is_mine(self):
        return Member.current().id == self.sender_id

    def to_dict(self):
        message_dictionary = super().to_dict()
        message_dictionary.update(isMine=self.is_mine)
        message_dictionary.update(activated_at=self.activated_at)
        return message_dictionary

    @classmethod
    def json_metadata(cls):
        is_mine = Field(Boolean, not_none=True, readonly=True)
        metadata = super().json_metadata()
        metadata['fields']['isMine'] = is_mine.info
        return metadata

    __mapper_args__ = {
        'polymorphic_identity' : 'message',
    }

