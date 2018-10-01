import json as json_library

from nanohttp import RestController, json, context, HTTPBadRequest, validate, \
    HTTPForbidden, settings
from restfulpy.authorization import authorize
from restfulpy.orm import DBSession

from ..backends import CASClient
from ..models import User


class TokenController(RestController):

    @validate(
        email=dict(required='400 Invalid email or password')
    )
    @json
    def create(self):
        email = context.form.get('email')
        principal = context.application.__authenticator__.login(email)
        if principal is None:
            raise HTTPBadRequest('Invalid email or password')
        return dict(token=principal.dump())

    @authorize
    @json
    def invalidate(self):
        context.application.__authenticator__.logout()
        return {}

    @json(prevent_form='711 Form Not Allowed')
    def request(self):
        return dict(
            scopes=['email', 'title'],
            applicationId=settings.oauth['application_id'],
        )

    @json
    def obtain(self):
        cas_server = CASClient()
        access_token, member_id = cas_server \
            .get_access_token(context.form.get('authorizationCode'))

        member = cas_server.get_member(access_token)
        user = DBSession.query(User) \
            .filter(User.email == member['email']) \
            .one_or_none()

        if user is None:
            user = User(
                email=member['email'],
                title=member['title'],
                access_token=access_token,
                reference_id=member['id']
            )
        else:
            user.access_token = access_token

        DBSession.add(user)
        DBSession.commit()
        principal = user.create_jwt_principal()
        context.response_headers.add_header(
            'X-New-JWT-Token',
            principal.dump().decode('utf-8')
        )

        return dict(token=principal.dump().decode('utf-8'))

