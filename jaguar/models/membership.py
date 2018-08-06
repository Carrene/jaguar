
import os
import uuid
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

contact = Table(
    'contact',
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
        primary_key=True,
    ),
)


class Member(
    ActivationMixin,
    SoftDeleteMixin,
    ModifiedMixin,
    OrderingMixin,
    FilteringMixin,
    PaginationMixin,
    DeclarativeBase
):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    email = Field(
        Unicode(100),
        unique=True,
        index=True,
        json='email',
        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    )
    _password = Field(
        'password',
        Unicode(128),
        index=True,
        json='password',
        protected=True,
        min_length=6
    )
    title = Field(Unicode(100))
    type = Field(Unicode(50))

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type,
    }

    @property
    def roles(self):
        return []

    @classmethod
    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hashed_pass = sha256()
        # Make sure password is a str because we cannot hash unicode objects
        hashed_pass.update((password + salt).encode('utf-8'))
        hashed_pass = hashed_pass.hexdigest()

        password = salt + hashed_pass
        return password

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        min_length = self.__class__.password.info['min_length']
        if len(password) < min_length:
            raise HTTPStatus(
                f'704 Please enter at least {min_length} characters '
                'for password.'
            )
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym(
        '_password',
        descriptor=property(_get_password, _set_password),
        info=dict(protected=True)
    )

    def validate_password(self, password):
        hashed_pass = sha256()
        hashed_pass.update((password + self.password[:64]).encode('utf-8'))
        return self.password[64:] == hashed_pass.hexdigest()

    def create_jwt_principal(self, session_id=None):
        # FIXME: IMPORTANT Include user password as salt in signature

        if session_id is None:
            session_id = str(uuid.uuid4())

        return JwtPrincipal(dict(
            id=self.id,
            roles=self.roles,
            email=self.email,
            sessionId=session_id,
            name=self.title
        ))

    @classmethod
    def activate(cls, token):
        serializer = itsdangerous.URLSafeTimedSerializer(
            settings.activation.secret
        )

        try:
            email = serializer.loads(
                token,
                max_age=settings.activation.max_age
            )

        except itsdangerous.SignatureExpired:
            raise HTTPConflict(reason='signature-expired')

        except itsdangerous.BadSignature:
            raise HTTPBadRequest('Invalid Token')

        query = DBSession.query(Member)

        member = cls.exclude_deleted(query).filter(cls.email == email).one()
        if member.is_active:
            raise HTTPConflict('Member is already activated.')
        member.is_active = True
        return member

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
        json='phone',
        nullable=True,
        min_length=10,
        watermark='Phone',
        example='734 555 1212',
        pattern='\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}'
        '[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}',
    )
    show_email = Field(Boolean, default=False)
    show_phone = Field(Boolean, default=False)
    contacts = relationship(
        'User',
        secondary=contact,
        primaryjoin=id == contact.c.source,
        secondaryjoin=id == contact.c.destination,
    )
    user_room = relationship('Room', backref='owner')
    blocked_users = relationship(
        'User',
        secondary=blocked,
        primaryjoin=id == blocked.c.source,
        secondaryjoin=id == blocked.c.destination,
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

    def create_jwt_principal(self, session_id=None):
        principal = super().create_jwt_principal(session_id=session_id)
        return principal

