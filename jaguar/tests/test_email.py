from bddrest.authoring import response, when, Remove, Update

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestEmail(AutoDocumentationBDDTest):

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

    def test_claim_email(self):
        with self.given(
            'claim a user',
            '/apiv1/emails',
            'CLAIM',
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

