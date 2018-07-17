from bddrest.authoring import response, when, Remove, Update
from jaguar.models.membership import User
from restfulpy.orm import DBSession
from restfulpy.testing import ApplicableTestCase

from ..controllers.root import Root


class TestMembership(ApplicableTestCase):
    __controller_factory__ = Root
    __configuration__ = '''
    reset_password:
      secret: reset-password-secret
      max_age: 3600  # seconds
      url: http://nc.carrene.com/reset_password
      # url: http://localhost:8080/reset_password

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
            user_name = 'example',
        )
        DBSession.add(user)
        DBSession.commit()

    def test_registration(self):
        with self.given(
            'claim a user',
            url='/apiv1/members',
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



