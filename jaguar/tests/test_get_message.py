
from bddrest import when, status, response, Update

from jaguar.models import User, Message, Room
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestGetUser(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.message1 = Message(
            body='This is message 1',
            mime_type='text/plain'
        )
        cls.message2 = Message(
            body='This is message 2',
            mime_type='text/plain'
        )
        cls.message3 = Message(
            body='This is message 3',
            mime_type='text/plain'
        )
        user1 = User(
            email='user1@example.com',
            title='user1',
            username='user1',
            access_token='access token1',
            reference_id=2,
            messages=[cls.message1]
        )
        user2 = User(
            email='user2@example.com',
            title='user2',
            username='user2',
            access_token='access token2',
            reference_id=3,
            messages=[cls.message3, cls.message2]
        )
        room1 = Room(
            title='room1',
            members=[user1, user2],
            messages=[cls.message1, cls.message3]
        )
        room2 = Room(title='room2', members=[user2], messages=[cls.message2])
        session.add(user1)
        session.commit()

    def test_get_user_by_id(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            f'Get a message by id',
            f'/apiv1/messages/id:{self.message1.id}',
            f'GET',
        ):
            assert status == 200
            assert response.json['body'] == 'This is message 1'

            when(
                'get The message sent by another user in the same room',
                url_parameters=Update(id=f'{self.message3.id}')
            )
            assert status == 200
            assert response.json['body'] == 'This is message 3'

            when('Ivalid message id', url_parameters=Update(id='message1'))
            assert status == 707

            when('Message not found', url_parameters=Update(id=5))
            assert status == '614 Message Not Found'

            when(
                'Try to get a message from an unsubscribe target',
                url_parameters=Update(id=f'{self.message2.id}')
            )
            assert status == 403

            when('Try to pass unauthorize request', authorization=None)
            assert status == 401

