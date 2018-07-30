import itsdangerous
from bddrest.authoring import response, when, Update
from nanohttp import settings
from restfulpy.orm import DBSession

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMembership(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        user = User(
            email='already.added@example.com',
            title='example',
            password='123456',
        )
        user.is_active = True
        DBSession.add(user)
        DBSession.commit()

    def test_registration(self):
        serializer \
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

