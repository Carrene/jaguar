import itsdangerous
from bddrest.authoring import response, when, Update
from nanohttp import settings

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMembership(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='already.added@example.com',
            title='example',
            access_token='access token',
        )
        session.add(user)
        session.commit()

    def test_registration(self):
        serializer \
            = itsdangerous.URLSafeTimedSerializer(settings.activation.secret)
        token = serializer.dumps('test@example.com')
        with self.given(
            'Invalid password format',
            '/apiv1/users',
            'REGISTER',
            form=dict(token=token, title='test user')
        ):
            assert response.status == 704
            when('Registering a user', form=Update(password='123456'))
            assert response.status == 200
            assert 'X-New-JWT-Token' in response.headers[1]
            when('Invalid token', form=Update(token='Invalid token'))
            assert response.status == 703

