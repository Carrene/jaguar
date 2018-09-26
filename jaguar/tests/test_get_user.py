from bddrest import when, status, response, Update

from jaguar.models import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


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
        user2 = User(
            email='user2@example.com',
            title='user2',
            username='user2',
            access_token='access token'
        )
        session.add(user2)
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

            when('User not found', url_parameters=Update(id='3'))
            assert status == 404

            when('Ivalid use id', url_parameters=Update(id='user1'))
            assert status == 404

            when('Try to pass unauthorize request', authorization=None)
            assert status == 401

