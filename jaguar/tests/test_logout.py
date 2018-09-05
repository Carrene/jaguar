
from bddrest.authoring import response, when, Remove, Update, status

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestLogout(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='user@example.com',
            title='user',
            access_token='access token',
        )
        session.add(user)
        session.commit()

    def test_logout_a_user(self):
        self.login(
            dict(email='user@example.com'),
            '/apiv1/tokens',
            'CREATE'
        )

        with self.given(
            'Log out a user',
            '/apiv1/tokens',
            'INVALIDATE',
        ):
            assert status == 200

            when('Try to access some authorize source')
            assert status == 401

