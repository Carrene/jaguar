from bddrest.authoring import when, response, Remove, Update, status
from restfulpy.orm import DBSession

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMembership(AutoDocumentationBDDTest):

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
            assert status == 400

            when(
                'Request without password parameters',
                form=Remove('password')
            )
            assert status == 400

