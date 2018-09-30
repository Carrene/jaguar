from contextlib import contextmanager

from bddrest.authoring import given, status, response, when, Update, Remove
from restfulpy.principal import JwtPrincipal
from restfulpy.mockup import mockup_http_server
from nanohttp import settings, json
from nanohttp import RegexRouteController

from jaguar.tests.helpers import AutoDocumentationBDDTest, MockupApplication


@contextmanager
def cas_mockup_server():


    class Root(RegexRouteController):

        def __init__(self):
            super().__init__([
                ('/apiv1/members/me', self.get),
            ])

        @json
        def get(self):
            return dict(id=1, email='user1@example.com', title='user1')

    app = MockupApplication('cas-mockup', Root())
    with mockup_http_server(app) as (server, url):
        settings.merge(f'''
          tokenizer:
            url: {url}
        ''')
        yield app


class TestCasMemeber(AutoDocumentationBDDTest):

    def test_get_cas_member(self):
        token = JwtPrincipal(dict(
            email='user1@example.com',
            title='user1',
            referenceId='1'
        )).dump().decode()

        with cas_mockup_server():
            import pudb; pudb.set_trace()  # XXX BREAKPOINT
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
                    f'authorization: {token}',
                    'X-Access-Token: access token'
                }
            ):
                assert status == 200

                mismathc_token = JwtPrincipal(dict(
                    email='user2@example.com',
                    title='user2',
                    referenceId='2'
                )).dump().decode()

                when(
                    'Token not match the CAS member',
                    authorization=mismathc_token
                )
                assert status == 401

                when(
                    'Try to pass with bad token',
                    authorization='Invalid Token'
                )
                assert status == 400

#                when(
#                    'Try to access an unauthorized resource',
#                    authorization=None
#                )
#                assert status == 401

