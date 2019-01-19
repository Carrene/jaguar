from sqlalchemy import Unicode
from restfulpy.orm import Field

from .envelop import Envelop


class Mention(Envelop):

    __mapper_args__ = {'polymorphic_identity': 'mention'}

    reference = Field(
        Unicode(512),
        label='Reference',
        message='Lorem Ipsum',
        required=False,
        python_type=str,
        nullable=True,
        not_none=False,
        watermark='Lorem Ipsum',
        example='Lorem Ipsum',
    )

