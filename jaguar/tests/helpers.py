from os import path, makedirs
from contextlib import contextmanager

from restfulpy.application import Application
from bddrest.authoring import response
from restfulpy.testing import ApplicableTestCase
from restfulpy.orm import DBSession
from restfulpy.mockup import mockup_http_server
from nanohttp import RegexRouteController, json, settings, context, HTTPStatus
from restfulpy.orm.metadata import FieldInfo

from jaguar import Jaguar
from jaguar.authentication import Authenticator
from jaguar.controllers.root import Root
from jaguar.models import Member, Room, Message


HERE = path.abspath(path.dirname(__file__))
DATA_DIRECTORY = path.abspath(path.join(HERE, '../../data'))


_cas_server_status = 'idle'


query=FieldInfo(type_=str, required=True, not_none=True).to_json()
user_id=FieldInfo(type_=str, required=True, not_none=True).to_json()
member_id=FieldInfo(type_=str, required=True, not_none=True).to_json()
authorization_code=FieldInfo(type_=str, required=True, not_none=True).to_json()


room_fields = Room.json_metadata()['fields']
member_fields = dict(query=query)
contact_fields = dict(userId=user_id)
target_fields = dict(userId=user_id, memberId=member_id)
target_fields.update(room_fields)
authorization_fields= dict(authorizationCode=authorization_code)


class AutoDocumentationBDDTest(ApplicableTestCase):
    __application_factory__ = Jaguar
    __story_directory__ = path.join(DATA_DIRECTORY, 'stories')
    __api_documentation_directory__ = path.join(DATA_DIRECTORY, 'markdown')
    __configuration__ = '''
        authentication:
          redis:
            host: localhost
            port: 6379
            password: ~
            db: 15
    '''
    __metadata__ = {
        r'^/apiv1/members.*': member_fields,
        r'^/apiv1/contacts.*': contact_fields,
        r'^/apiv1/rooms.*': target_fields,
        r'^/apiv1/directs.*': target_fields,
        r'^/apiv1/messages.*': Message.json_metadata()['fields'],
        r'^/apiv1/oauth2/tokens.*': authorization_fields,
    }

    def login(self, email, url='/apiv1/tokens', verb='CREATE'):
        session = self.create_session()
        member = session.query(Member).filter(Member.email == email).one()
        token = member.create_jwt_principal().dump()
        self._authentication_token = token.decode()


@contextmanager
def cas_mockup_server():

    class Root(RegexRouteController):

        def __init__(self):
            super().__init__([
                ('/apiv1/members/me', self.get),
            ])

        @json
        def get(self):
            access_token = context.environ['HTTP_AUTHORIZATION']
            if _cas_server_status != 'idle':
                raise HTTPStatus(_cas_server_status)

            if 'access token1' in access_token:
                return dict(id=2, email='user1@example.com', title='user1')

            if 'access token2' in access_token:
                return dict(id=3, email='user2@example.com', title='user2')

            if 'access token3' in access_token:
                return dict(
                    id=4,
                    email='blocked1@example.com',
                    title='blocked1'
                )

            if 'access token4' in access_token:
                return dict(
                    id=5,
                    email='blocker@example.com',
                    title='blocker'
                )

            return dict(id=1, email='user@example.com', title='user')

    app = MockupApplication('cas-mockup', Root())
    with mockup_http_server(app) as (server, url):
        settings.merge(f'''
          tokenizer:
            url: {url}
          oauth:
              url: {url}
        ''')

        yield app


@contextmanager
def cas_server_status(status):
    global _cas_server_status
    _cas_server_status = status
    yield
    _cas_server_status = 'idle'


class MockupApplication(Application):

    def __init__(self, application_name, root):
        super().__init__(application_name,  root=root)
        self.__authenticator__ = Authorization()


class Authorization(Authenticator):

    def validate_credentials(self, credentials):
        pass

    def create_refresh_principal(self, member_id=None):
        pass

    def create_principal(self, member_id=None, session_id=None, **kwargs):
        pass

    def authenticate_request(self):
        pass

