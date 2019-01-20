from sqlalchemy import Unicode
from restfulpy.orm import Field

from .envelop import Envelop


class Mention(Envelop):

    __mapper_args__ = {'polymorphic_identity': 'mention'}

