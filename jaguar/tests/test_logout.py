
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
            email='already.added@example.com',
            password='123456',

            url='/apiv1/tokens',
            verb='CREATE'
        )
        with self.given(
            'Log out a user',
            verb='INVALIDATE',
            url='/apiv1/tokens'
        ):
            assert status == 200
            when('Try to access some authorize source')
            assert status == 401

