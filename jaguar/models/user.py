from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, TimestampMixin,\
    ActivationMixin, ModifiedMixin, relationship
from restfulpy.taskqueue import Task
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger

from .envelop import Envelop


class User(DeclarativeBase):
    __tablename__ = 'user'

    id = Field(Integer, primary_key=True)

    title = Field(
        Unicode(50),
        json = 'title'
    )

    envelop_id = relationship('Envelop')

    user_name = Field(
        Unicode(50),
        unique=True,
        index = True,
    )

    email = Field(
        Unicode(100),
        unique=True,
        index=True,
        json='email',
        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        watermark='Email',
        example="user@example.com"
    )

    phone = Field(
        Unicode(50),
        nullable=True,
        json='phone',
        min_length=10,
        watermark='Phone',
        example='734 555 1212',
        pattern=r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}'
            r'[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}',
    )
