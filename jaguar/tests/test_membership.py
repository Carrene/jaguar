import itsdangerous
from bddrest.authoring import response, when, Update
from nanohttp import settings
from restfulpy.application import Application
from restfulpy.orm import DBSession
from restfulpy.testing import ApplicableTestCase

from ..controllers.root import Root
from jaguar.authentication import Authenticator
from jaguar.models.membership import User

from.helpers import AutoDocumentationBDDTest


class TestMembership(AutoDocumentationBDDTest):
    __application__ = Application(
        'Mockup',
        root=Root(),
        authenticator=Authenticator()
    )

    __configuration__ = '''

    activation:
      secret: activation-secret
      max_age: 86400  # seconds
      url: http://nc.carrene.com/activate
      # url: http://localhost:8080/activate
    '''

    @classmethod
    def mockup(cls):
        user = User(
            email='already.added@example.com',
            title = 'example',
            password = '123456',
        )
        user.is_active = True
        DBSession.add(user)
        DBSession.commit()

    def test_registration(self):
        serializer\
            = itsdangerous.URLSafeTimedSerializer(settings.activation.secret)
        token = serializer.dumps('test@example.com')

        with self.given(
            'Invalid password format',
            verb='REGISTER',
            url='/apiv1/members',
            form=dict(token=token, password='1234', title='test member')
        ):
            assert response.status == 704

            when('Registering a user', form=Update(password='123456'))
            assert response.status == 200
            assert 'X-New-JWT-Token' in response.headers[1]

            when('Invalid token', form=Update(token='Invalid token'))
            assert response.status == 703

