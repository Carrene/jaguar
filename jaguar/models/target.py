from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, ModifiedMixin
from restfulpy.taskqueue import Task
from restfulpy.logging_ import get_logger
from sqlalchemy import Integer, ForeignKey, Unicode, BigInteger, Table,\
    Column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from jaguar.models.user import User


class Target(DeclarativeBase, ModifiedMixin):
    __tablename__  = 'target'

    id = Field(Integer, primary_key=True)

    title = Field(
        Unicode(50),
        nullable = True,
        json = 'title'
    )
    type = Field(
        Unicode(25)
    )

    __mapper_args__ = {
        'polymorphic_identity' :__tablename__,
        'polymorphic_on' : type,
    }


class Room(Target):
    __tablename__ = 'room'

    id = Field (
        Integer,
        ForeignKey('target.id'),
        primary_key = True,
        json = 'target_id'
    )

#    members = relationship(
#        'User',
#        secondary=association_table ,
#        back_populates ='rooms'
#    )


    __mapper_args__ = {
        'polymorphic_identity' : __tablename__,
    }


class Direct(Target):
    __tablename__ = 'direct'

    id = Field (
        Integer,
        ForeignKey('target.id'),
        primary_key = True,
        json = 'target_id'
    )

    __mapper_args__ = {
        'polymorphic_identity' : __tablename__,
    }

