from restfulpy.authentication import StatefulAuthenticator
from nanohttp import HTTPConflict, HTTPBadRequest
from restfulpy.authentication import StatefulAuthenticator
from restfulpy.orm import DBSession

from .models import Member


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

