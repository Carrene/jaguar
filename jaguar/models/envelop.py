
from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin,relationship,\
    ActivationMixin, OrderingMixin, FilteringMixin, PaginationMixin, \
    SoftDeleteMixin
from restfulpy.orm.metadata import FieldInfo
from restfulpy.taskqueue import RestfulpyTask
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table, \
    Boolean, JSON
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy_media import File, MagicAnalyzer, ContentTypeValidator

from .membership import Member


user_message = Table(
    'user_message',
    DeclarativeBase.metadata,
    Field('message_id', Integer, ForeignKey('envelop.id')),
    Field('user_id', Integer, ForeignKey('user.id')),
)


class FileAttachment(File):
    __pre_processors__ = [
        MagicAnalyzer(),
        ContentTypeValidator(['image/jpeg', 'image/png', 'text/plain'])
    ]


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


is_mine_fieldinfo = FieldInfo(Boolean, not_none=True, readonly=True)


class Message(Envelop):

    mimetype = Field(Unicode(25))

    # A message can be a reply to another message, so The id of
    # the source message is set in reply_root
    reply_root = Field(Integer, ForeignKey('envelop.id'), nullable=True)

    _attachment = Field(
        FileAttachment.as_mutable(JSON),
        nullable=True,
        label='Attachment'
    )

    @property
    def attachment(self):
        return self._attachment.locate() if self._attachment else None

    @attachment.setter
    def attachment(self, value):
        if value is not None:
            self._attachment = FileAttachment.create_from(value)
        else:
            self._attachment = None


    # Since this relationship should be a many to one relationship,
    # The remote_side is declared
    reply_to = relationship(
        'Message',
        remote_side=[Envelop.id],
        protected=False
    )

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
        metadata = super().json_metadata()
        metadata['fields']['isMine'] = is_mine_fieldinfo.to_json()
        return metadata

    __mapper_args__ = {
        'polymorphic_identity' : 'message',
    }

