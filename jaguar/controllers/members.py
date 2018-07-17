from typing import Union
import re
import itsdangerous

from nanohttp import RestController, json, HTTPNotFound, context,\
    HTTPMethodNotAllowed, HTTPBadRequest, HTTPConflict,HTTPUnauthorized,\
    HTTPForbidden, HTTPStatus
from nanohttp import settings
from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession
from restfulpy.controllers import ModelRestController
from restfulpy.logging_ import get_logger

from jaguar.models import Member, User, ActivationEmail
from jaguar.fun import EmptyJsonResponse


logger = get_logger('membership')
MemberId = Union[int, str]


class MembersController(ModelRestController):
    """

    Activate:                   GET ?t_={token}
    Resend Activation:          POST /me/activation
    Fetch one:                  GET /{member_id}
    Fetch me:                   GET /me
    Signup:                     POST /
    Change Password:            PUT /me/password
    Request Reset Password:     PATCH /me/password
    Reset Password:             DELETE /me/password

    """
    __model__ = Member

    @json
    @commit
    def claim(self):
        email = context.form.get('email')

        email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

        if not email:
            raise HTTPBadRequest()

        if not re.match(email_pattern, email):
            raise HTTPStatus('701 Invalid email format.')

        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPStatus(
                '601 The requested email address is already registered.'
            )

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.activation.secret)

        token = serializer.dumps(email)

        DBSession.add(
            ActivationEmail(
                to=email,
                subject='Activate your NueMD Coder account',
                body={
                    'activation_token': token,
                    'activation_url': settings.activation.url
                }
            )
        )

        return dict()

