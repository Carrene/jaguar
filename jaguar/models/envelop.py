
from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin,relationship,\
    ActivationMixin
from restfulpy.taskqueue import RestfulpyTask
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table
from sqlalchemy.dialects.postgresql.json import JSONB


user_message = Table(
    'user_message',
    DeclarativeBase.metadata,
    Field('message_id', Integer, ForeignKey('message.id')),
    Field('user_id', Integer, ForeignKey('user.id')),
)


class Envelop(ActivationMixin, ModifiedMixin, DeclarativeBase):
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
    __tablename__ = 'message'

    id = Field(
        Integer,
        ForeignKey('envelop.id'),
        primary_key=True,
    )
    mime_type=Field(Unicode(25))

    # Since collections would be fairly small,
    # selecin loding is chosen for this relationship.
    seen_by = relationship(
        'User',
        secondary=user_message,
        lazy='selectin'
    )
    __mapper_args__ = {
        'polymorphic_identity' : __tablename__,
    }

