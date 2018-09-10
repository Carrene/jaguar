from os import path, makedirs

from restfulpy.application import Application
from bddrest.authoring import response
from restfulpy.testing import ApplicableTestCase
from restfulpy.orm import DBSession

from jaguar import Jaguar
from jaguar.authentication import Authenticator
from jaguar.controllers.root import Root
from jaguar.models.membership import User


HERE = path.abspath(path.dirname(__file__))
DATA_DIRECTORY = path.abspath(path.join(HERE, '../../data'))


class AutoDocumentationBDDTest(ApplicableTestCase):

    __application_factory__ = Jaguar
    __story_directory__ = path.join(DATA_DIRECTORY, 'stories')
    __api_documentation_directory__ = path.join(DATA_DIRECTORY, 'markdown')

    def login(self, email, url='/apiv1/tokens', verb='CREATE'):
        super().login(dict(email=email), url = url, verb = verb)


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

