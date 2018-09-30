from contextlib import contextmanager

from bddrest.authoring import given, status, response, when, Update, Remove
from restfulpy.principal import JwtPrincipal
from restfulpy.mockup import mockup_http_server
from nanohttp import settings, json, context
from nanohttp import RegexRouteController

from jaguar.tests.helpers import AutoDocumentationBDDTest, MockupApplication, \
    cas_mockup_server
from jaguar.models import User


class TestCasMemeber(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@gmail.com',
            title='user1',
            reference_id=1,
            access_token='access token1'
        )
        session.add(user1)
        session.commit()

    def test_get_cas_member(self):
        token = JwtPrincipal(dict(
            email='user2@example.com',
            title='user2',
            referenceId=2
        )).dump().decode()
        self._authentication_token = token

        with cas_mockup_server():
            settings.merge(f'''
                oauth:
                  member:
                    url: {settings.tokenizer.url}/apiv1/members
                    verb: get
            ''')
            with self.given(
                title='Try to access an authorized resource',
                description='Members are got from the cas',
                url='/apiv1/index',
                headers={
                    'X-Access-Token: access token2'
                }
            ):
                assert status == 200

                mismathc_token = JwtPrincipal(dict(
                    email='user3@example.com',
                    title='user3',
                    referenceId=3
                )).dump().decode()

                when(
                    'Token not match the CAS member',
                    authorization=mismathc_token
                )
                assert status == 400

                when(
                    'Try to pass with bad token',
                    authorization='Invalid Token'
                )
                assert status == 400

                when(
                    'Try to access an unauthorized resource',
                    authorization=None
                )
                assert status == 401

                member_token = JwtPrincipal(dict(
                    email='user1@example.com',
                    title='user1',
                    referenceId=1
                )).dump().decode()
                when(
                    'User exist in database',
                    authorization=member_token
                )
                assert status == 200

