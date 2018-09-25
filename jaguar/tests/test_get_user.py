from bddrest import given, when, status, response, Update

from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.models import User


class TestGetUser(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            title='user1',
            username='user1',
            access_token='access token',
        )
        session.add(user1)
        session.commit()

    def test_get_user_by_id(self):
        self.login('user1@example.com')

        with self.given(
            'Get a user by her or his id',
            '/apiv1/users/id:1',
            'GET',
        ):
            assert status == 200
            assert response.json['title'] == 'user1'

            when('User not found', url_parameters=Update(id='2'))
            assert status == 404

            when('Ivalid use id', url_parameters=Update(id='user1'))
            assert status == 404

            when('Try to pass unauthorize request', authorization=None)
            assert status == 401

