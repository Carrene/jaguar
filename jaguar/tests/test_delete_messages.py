from bddrest.authoring import when, status, response, Update

from jaguar.models import User, Room, Message
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestDeleteMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        cls.session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            password='123456',
            title='user1'
        )
        user2 = User(
            email='user2@example.com',
            password='123456',
            title='user2'
        )
        room = Room(title='room', type='room')
        room.members.append(user1)
        cls.session.add(user2)
        cls.session.add(room)
        cls.session.flush()
        message1 = Message(body='This is message 1', mime_type='text/plain')
        message2 = Message(body='This is message 2', mime_type='text/plain')
        message1.target_id = room.id
        message1.sender_id = user1.id
        message2.target_id = room.id
        message2.sender_id = user1.id
        cls.session.add_all([message1, message2])
        cls.session.commit()

    def test_delete_the_message(self):
        self.login(
            email='user1@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Try to delete a message',
            '/apiv1/messages/id:1',
           'DELETE'
        ):
            assert status == 200
            assert response.json['body'] == 'This is message 1'
            assert len(self.session.query(Message).all()) == 1

            when('The message not exists', url_parameters=Update(id=3))
            assert status == '614 Message Not Found'

            when(
                'Trying to pass using invalid message id',
                url_parameters=Update(id='Invalid')
            )
            assert status == '707 Invalid MessageId'

    # TODO: More test scenarios should be checked when other
    #authorizations would be implemented
    def test_forbidden_request(self):
        self.login(
            email='user2@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Not allowed to delete the message',
            '/apiv1/messages/id:2/',
            'DELETE',
         ):
             assert status == 403

