from restfulpy.authentication import StatefulAuthenticator
from nanohttp import HTTPConflict, HTTPBadRequest, context, HTTPUnauthorized
from restfulpy.authentication import StatefulAuthenticator
from restfulpy.orm import DBSession
from cas import CASPrincipal

from .models import Member, User
from .backends import CASClient


class Authenticator(StatefulAuthenticator):

    @staticmethod
    def safe_member_lookup(condition):
        query = DBSession.query(Member)
        member = Member.exclude_deleted(query).filter(condition).one_or_none()
        if member is None:
            raise HTTPBadRequest()

        return member

    def create_principal(self, member_id=None):
        member = self.safe_member_lookup(Member.id == member_id)
        return member.create_jwt_principal()

    def create_refresh_principal(self, member_id=None):
        member = self.safe_member_lookup(Member.id == member_id)
        return member.create_refresh_principal()

    def validate_credentials(self, credentials):
        email = credentials
        member = self.safe_member_lookup(Member.email == email)
        return member

    def verify_token(self, encoded_token):
        principal = CASPrincipal.load(encoded_token)
        member = DBSession.query(User) \
            .filter(User.reference_id == principal.reference_id) \
            .one_or_none()
        if not member and not 'HTTP_X_OAUTH2_ACCESS_TOKEN' in context.environ:
            raise HTTPBadRequest()

        access_token = member.access_token if member \
            else context.environ['HTTP_X_OAUTH2_ACCESS_TOKEN']

        cas_member = CASClient().get_member(access_token)
        if cas_member['email'] != principal.email:
            raise HTTPBadRequest()

        if member is None:
            DBSession.add(User(
                    email=cas_member['email'],
                    title=cas_member['title'],
                    reference_id=cas_member['id'],
                    access_token=access_token
            ))
        elif member.title != cas_member['title']:
            member.title = cas_member['title']

        DBSession.commit()
        return principal

