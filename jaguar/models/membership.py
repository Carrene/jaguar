from cas import CASPrincipal
from nanohttp import context
from restfulpy.orm import DeclarativeBase, Field, ModifiedMixin, \
    ActivationMixin, SoftDeleteMixin, relationship, DBSession, \
    FilteringMixin, PaginationMixin, OrderingMixin
from restfulpy.principal import JwtRefreshToken
from sqlalchemy import Unicode, Integer, ForeignKey, Boolean, Table


member_block = Table(
    'blocked',
    DeclarativeBase.metadata,
    Field(
        'member_id',
        Integer,
        ForeignKey('member.id'),
        primary_key=True,
    ),
    Field(
        'blocked_member_id',
        Integer,
        ForeignKey('member.id'),
        primary_key=True
    )
)


class MemberContact(DeclarativeBase):
    __tablename__ = 'member_contact'

    member_id = Field(Integer, ForeignKey('member.id'), primary_key=True)
    contact_member_id = Field(Integer, ForeignKey('member.id'), primary_key=True)


class Member(ActivationMixin, SoftDeleteMixin, ModifiedMixin, OrderingMixin,
             FilteringMixin, PaginationMixin, DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    reference_id = Field(Integer, unique=True)
    email = Field(
        Unicode(100),
        unique=True,
        index=True,
        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    )
    access_token = Field(Unicode(200), protected=True)

    # FIXME: What is this?
    add_to_room = Field(Boolean, default=True)
    title = Field(
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
        pattern=r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}'
            r'[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}',
    )
    show_email = Field(Boolean, default=False)
    show_phone = Field(Boolean, default=False)
    messages = relationship('Envelop')
    contacts = relationship(
        'Member',
        secondary='member_contact',
        primaryjoin=id == MemberContact.member_id,
        secondaryjoin=id == MemberContact.contact_member_id,
        lazy='selectin'
    )
    room = relationship('Room', back_populates='owner')
    blocked_members = relationship( 'Member',
        secondary=member_block,
        primaryjoin=id == member_block.c.member_id,
        secondaryjoin=id == member_block.c.blocked_member_id,
        lazy='selectin'
    )

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
            .filter(cls.reference_id == context.identity.reference_id).one()

    def to_dict(self):
        member_dict = super().to_dict()
        member_dict['phone'] = self.phone if self.show_phone else None
        member_dict['email'] = self.email if self.show_email else None
        return member_dict

    @property
    def roles(self):
        return ['member']

