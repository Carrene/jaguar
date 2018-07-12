from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, TimestampMixin,\
    ActivationMixin, ModifiedMixin
from restfulpy.taskqueue import Task
from restfulpy.logging_ import get_logger
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger
from sqlalchemy.orm import relationship

# from . import assosiation

class User(DeclarativeBase):
    __tablename__ = 'user'

    id = Field(Integer, primary_key=True)

    title = Field(
        Unicode(50),
        json = 'title'
    )

    user_name = Field(
        Unicode(50),
        unique=True,

    )

    email = Field(
        Unicode(50),
        unique=True,
        index=True,
        nullable=True,
        json='email',
        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    )

#    rooms = relationship(
#        'Room',
#        secondary=assosiation.association_table,
#        back_populates='members',
#    )

    phone = Field(BigInteger, unique=True, nullable=True)





