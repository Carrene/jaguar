from bddrest.authoring import response, when, Remove, Update
from restfulpy.orm import DBSession

from jaguar.models.membership import User

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestEmail(AutoDocumentationBDDTest):

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

    def test_claim_email(self):
        with self.given(
            'claim a user',
            url='/apiv1/emails',
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

