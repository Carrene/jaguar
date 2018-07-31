
from typing import Union

import itsdangerous
from nanohttp import json, context, HTTPStatus, settings
from restfulpy.controllers import ModelRestController
from restfulpy.logging_ import get_logger
from restfulpy.orm import DBSession

from jaguar.models import Member


class MemberController(ModelRestController):
    __model__ = Member

    @json
    def register(self):

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.activation.secret)

        try:
            email = serializer.loads(
                context.form.get('token'),
                max_age=settings.activation.max_age
            )

        except itsdangerous.BadSignature:
            raise HTTPStatus(status='703 Invalid email activation token')

        member = Member(
            email=email,
            title=context.form.get('title'),
            password=context.form.get('password')
        )
        member.is_active = True
        DBSession.add(member)
        DBSession.commit()
        principal = member.create_jwt_principal()
        context.response_headers.add_header(
            'X-New-JWT-Token',
            principal.dump().decode('utf-8')
        )
        return member

