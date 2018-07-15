
from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin,relationship,\
    ActivationMixin
from restfulpy.taskqueue import Task
from restfulpy.logging_ import get_logger
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table
from sqlalchemy.dialects.postgresql.json import JSONB


class Envelop(ActivationMixin, ModifiedMixin, DeclarativeBase):
    __tablename__ = 'envelop'

    id = Field(Integer, primary_key=True)
    type = Field(Unicode(25))
    target_id = Field(Integer, ForeignKey('target.id'))
    sendder_id = Field(Integer, ForeignKey('user.id'))
    body = Field(JSONB)


