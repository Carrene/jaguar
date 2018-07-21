
from bddrest.authoring import when, response, Remove, Update
from restfulpy.application import Application
from restfulpy.orm import DBSession
from restfulpy.testing import ApplicableTestCase

from ..controllers.root import Root
from jaguar.authentication import Authenticator
from jaguar.models.membership import User


class TestMembership(ApplicableTestCase):
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

    def test_login(self):
        with self.given(
            'Login user',
            verb='CREATE',
            url='/apiv1/tokens',
            form=dict(email='already.added@example.com', password='123456')
        ):
            assert response.status == 200

            when('Invalid email', form=Update(email='user@example.com'))
            assert response.status == 400

            when(
                'Invalid password',
                form=Update(
                    email='already.added@example.com',
                    password='1234567'
                )
            )
            assert response.status == 400

            when('Request without email parameters', form=Remove('email'))
            assert response.status == 400

            when(
                'Request without password parameters',
                form=Remove('password')
            )
            assert response.status == 400

