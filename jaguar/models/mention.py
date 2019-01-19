from sqlalchemy import NVARCHAR

from .envelop import Envelop


class Mention(Envelop):

    __mapper_args__ = {'polymorphic_identity': 'mention'}

    reference = Field(
        NVARCHAR(512),
        label='Reference',
        message='Lorem Ipsum',
        required=True,
        python_type=str,
        nullable=False,
        not_none=True,
        watermark='Lorem Ipsum',
        example='Lorem Ipsum',
    )

