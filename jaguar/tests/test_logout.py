
from bddrest.authoring import response, when, Remove, Update, status

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestEmail(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='already.added@example.com',
            title='example',
            password='123456',
        )
        user.is_active = True
        session.add(user)
        session.commit()

    def test_logout(self):
        self.login(
            'already.added@example.com',
            '123456',
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

