
import os
from hashlib import sha256

import itsdangerous
from sqlalchemy.orm import backref
from sqlalchemy import Unicode, Integer, ForeignKey, Boolean, Table
from sqlalchemy.orm import synonym, validates
from sqlalchemy.events import event
from nanohttp import settings, HTTPBadRequest, HTTPNotFound, \
    context, HTTPConflict, ContextIsNotInitializedError, HTTPStatus
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from restfulpy.orm import DeclarativeBase, Field, ModifiedMixin, \
    ActivationMixin, SoftDeleteMixin, relationship, DBSession, \
    FilteringMixin, PaginationMixin, OrderingMixin
from cas import CASPrincipal

from .envelop import Envelop
from .messaging import ActivationEmail


blocked = Table(
    'blocked',
    DeclarativeBase.metadata,
    Field(
        'source',
        Integer,
        ForeignKey('user.id'),
        primary_key=True,
    ),
    Field(
        'destination',
        Integer,
        ForeignKey('user.id'),
        primary_key=True
    )
)


class Contact(DeclarativeBase):
    __tablename__ = 'contact'

    source = Field(Integer, ForeignKey('user.id'), primary_key=True)
    destination = Field(Integer, ForeignKey('user.id'), primary_key=True)


class Member(ActivationMixin, SoftDeleteMixin, ModifiedMixin,OrderingMixin,
             FilteringMixin, PaginationMixin, DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    reference_id = Field(Integer)
    email = Field(
        Unicode(100),
        unique=True,
        index=True,
        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    )
    title = Field(Unicode(100))
    access_token = Field(Unicode(200), protected=True)
    type = Field(Unicode(50))

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type,
    }

    @property
    def roles(self):
        return []

    def create_jwt_principal(self):
        return CASPrincipal(dict(
            id=self.id,
            roles=self.roles,
            email=self.email,
            name=self.title,
            referenceId=self.reference_id
        ))

    def create_refresh_principal(self):
        return JwtRefreshToken(dict(
            id=self.id
        ))

    @classmethod
    def current(cls):
        return DBSession.query(cls) \
            .filter(cls.email == context.identity.email).one()


class User(Member):
    __tablename__ = 'user'

    id = Field(Integer, ForeignKey('member.id'), primary_key=True)
    add_to_room = Field(Boolean, default=True)
    username = Field(
        Unicode(50),
        unique=True,
        index=True,
        nullable=True,
    )
    phone = Field(
        Unicode(50),
        nullable=True,
        min_length=10,
        watermark='Phone',
        example='734 555 1212',
        pattern='\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}'
            '[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}',
    )
    show_email = Field(Boolean, default=False)
    show_phone = Field(Boolean, default=False)
    messages = relationship('Envelop')
    contacts = relationship(
        'User',
        secondary='contact',
        primaryjoin=id == Contact.source,
        secondaryjoin=id == Contact.destination,
        lazy='selectin'
    )
    room = relationship('Room', back_populates='owner')
    blocked_users = relationship(
        'User',
        secondary=blocked,
        primaryjoin=id == blocked.c.source,
        secondaryjoin=id == blocked.c.destination,
        lazy='selectin'
    )

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            username=self.username,
            phone=self.phone if self.show_phone else None,
            email=self.email if self.show_email else None,
        )

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    @property
    def roles(self):
        return ['user']

