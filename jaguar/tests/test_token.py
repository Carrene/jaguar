from bddrest.authoring import when, response, Remove, Update, status

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestToken(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='already.added@example.com',
            title='user',
            access_token='access token',
        )
        session.add(user)
        session.commit()

    def test_login(self):
        with self.given(
            'Login user',
            '/apiv1/tokens',
            'CREATE',
            form=dict(email='already.added@example.com',)
        ):
            assert response.status == 200

            when('Invalid email', form=Update(email='user@example.com'))
            assert response.status == 400

            when('Request without email parameters', form=Remove('email'))
            assert status == 400


