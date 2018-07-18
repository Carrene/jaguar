
import itsdangerous

from bddrest.authoring import response, when, Remove, Update
from jaguar.models.membership import User
from restfulpy.orm import DBSession
from restfulpy.testing import ApplicableTestCase
from nanohttp import settings
from restfulpy.application import Application
from jaguar.authentication import Authenticator

from ..controllers.root import Root


class TestMembership(ApplicableTestCase):
    __application__ = Application(
        'Mockup',
        root=Root(),
        authenticator=Authenticator()
    )

    __configuration__ = '''
    reset_password:
      secret: reset-password-secret
      max_age: 3600  # seconds
      url: http://nc.carrene.com/reset_password
      # url: http://localhost:8080/reset_password

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
            user_name = 'example',
        )
        DBSession.add(user)
        DBSession.commit()

    def test_claim_email(self):
        with self.given(
            'claim a user',
            url='/apiv1/members',
            verb='CLAIM',
            form=dict(email='test@example.com')
        ):

            assert response.status == '200 OK'

            when(
                'The email is repeted',
                form=Update(email='already.added@example.com')
            )
            assert response.status == 601

            when(
                'The email format is invalid',
                form=Update(email='already.example.com')
            )
            assert response.status == 701

            when('Request without email', form=Remove('email'))
            assert response.status == 400

    def test_registration(self):
        serializer\
            = itsdangerous.URLSafeTimedSerializer(settings.activation.secret)
        token = serializer.dumps('test@example.com')

        with self.given(
            'Invalid password format',
            verb='REGISTER',
            url='/apiv1/members',
            form=dict(token=token, password='1234', title='test user')
        ):
            assert response.status == 704

            when('Registering a user',form=Update(password='123456'))
            assert response.status == 200
            assert 'token' in response.json

            when('Invalid token',form=Update(token='Invalid token'))
            assert response.status == 703























