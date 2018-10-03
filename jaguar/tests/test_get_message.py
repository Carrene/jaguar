
from bddrest import when, status, response, Update

from jaguar.models import User
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestGetUser(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        message1 = Message(
            body='This is message 1',
            mime_type='text/plain'
        )
        message2 = Message(
            body='This is message 2',
            mime_type='text/plain'
        )
        message3 = Message(
            body='This is message 3',
            mime_type='text/plain'
        )
        user1 = User(
            email='user1@example.com',
            title='user1',
            username='user1',
            access_token='access token1',
            reference_id=2
        )
        room1 = Room(title='room1', members=[user1])
        room2 = Room(title='room2', members=[user2])
        session.add(user1)
        session.commit()

    def test_get_user_by_id(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
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

