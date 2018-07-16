from typing import Union
import re

from nanohttp import RestController, json, HttpNotFound, context,\
    HttpMethodNotAllowed, HttpBadRequest, HttpConflict, HttpUnauthorized,\
    HttpForbidden
from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession
from restfulpy.controllers import ModelRestController
from restfulpy.logging_ import get_logger

from jaguar.models import Member, CasUser

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
#
#    @staticmethod
#    def validate_user_id(user_id) -> int:
#        try:
#            return int(user_id or '')
#        except ValueError:
#            raise HttpBadRequest()
#
#    @json
#    @Member.expose
#    @commit
#    def get(self, member_id: MemberId = None):
#        if 't_' in context.query_string:
#            token = context.query_string.get('t_')
#            if token:
#                return Member.activate(token)
#            logger.info('Bad request syntax or unsupported method member')
#            raise HttpBadRequest()
#
#        # Authorize after check token
#        identity = context.identity
#        if not identity:
#            raise HttpUnauthorized()
#
#        query = Member.exclude_deleted()
#
#        if member_id is None:
#            raise HttpNotFound()
#
#        elif member_id == 'me':
#            return Member.current()
#        else:
#            member_id = self.validate_user_id(member_id)
#            query = query.filter(Member.id == int(member_id))
#            if not context.identity.is_in_roles('god'):
#                query = query.filter(Member.id == identity.id)
#
#            c = query.one_or_none()
#            if not c:
#                logger.info('Nothing matches the given member URI.')
#                raise HttpNotFound()
#            return c

    @json
    @Member.expose
    @commit
    def post(self, member_id: MemberId = None, attribute: str = None):
        email = context.form.get('email')
        if not email:
            raise HttpBadRequest()

        if member_id == 'me' and attribute == 'activation':
            member = Member.exclude_deleted()\
                .filter(Member.email == email)\
                .one_or_none()

            if member is None:
                raise HttpNotFound()

            DBSession.add(member.send_activation_token())
            return EmptyJsonResponse

        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HttpConflict('The requested email address is already registered.')

        new_member = User()
        new_member.update_from_request()
        DBSession.add(new_member.send_activation_token())
        DBSession.add(new_member)
        return new_member
#
#    @json
#    @authorize
#    @commit
#    def put(self, user_id: MemberId, attribute: str = None):
#        if user_id == 'me' and attribute == 'password':
#            old_password = context.form.get('oldPassword')
#            password = context.form.get('password')
#            user = Member.current()
#            user.change_password(old_password, password)
#            return user
#
#        query = Member.exclude_deleted().filter(Member.id == user_id)
#        if not context.identity.is_in_roles('god'):
#            query = query.filter(Member.id == context.identity.id)
#        new_user = query.one_or_none()
#        if new_user is None:
#            raise HttpNotFound()
#
#        new_user.update_from_request()
#        return new_user
#
#    @json
#    @commit
#    def patch(self, member_id: MemberId = None, attribute: str = None):
#        if member_id == 'me' and attribute == 'password':
#            email = context.form.get('email')
#            if not email:
#                raise HttpBadRequest('Email address not exist.')
#
#            member = Member.exclude_deleted().filter(Member.email == email).one_or_none()
#            if not member:
#                raise HttpNotFound()
#
#            if not member.is_active:
#                raise HttpConflict('user-deactivated')
#
#            member.send_reset_password_token()
#            return EmptyJsonResponse
#
#        raise HttpMethodNotAllowed()
#
#    @json
#    @commit
#    def delete(self, user_id: MemberId = None, attribute: str = None):
#        if user_id == 'me' and attribute == 'password':
#            token = context.form.get('token')
#            password = context.form.get('password')
#
#            if not (token and password):
#                raise HttpBadRequest('Invalid member')
#
#            User.reset_password(token, password)
#            return EmptyJsonResponse
#
#        user_id = self.validate_user_id(user_id)
#
#        if not context.identity.is_in_roles('god', 'admin'):
#            raise HttpForbidden()
#
#        user = User.exclude_deleted().filter(User.id == user_id).one_or_none()
#        if user is None:
#            raise HttpNotFound()
#
#        user.soft_delete()
#        return user
#
#    @json
#    @Member.expose
#    @authorize('god', 'admin')
#    @commit
#    def undelete(self, user_id: int=None):
#        user_id = self.validate_user_id(user_id)
#        user = User.filter_deleted().filter(User.id == user_id).one_or_none()
#        if user is None:
#            raise HttpNotFound()
#
#        user.soft_undelete()
#        return user

