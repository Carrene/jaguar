from bddrest.authoring import when, status, response, Update

from jaguar.models import User, Room, Message
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestEditMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        cls.session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2
        )
        user2 = User(
            email='user2@example.com',
            title='user2',
            access_token='access token2',
            reference_id=3
        )
        room = Room(title='room', type='room')
        room.members.append(user1)
        cls.session.add(user2)
        cls.session.add(room)
        message1 = Message(
            body='This is message 1',
            mime_type='text/plain',
        )
        room.messages.append(message1)
        user1.messages.append(message1)
        message2 = Message(
            body='This is message 2',
            mime_type='text/plain',
        )
        room.messages.append(message2)
        user1.messages.append(message2)
        cls.session.commit()

    def test_edit_the_message(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Try to edit a message',
            '/apiv1/messages/id:1',
            'EDIT',
            form=dict(body='Message 1 is edited')
        ):
            assert status == 200
            assert response.json['body'] == 'Message 1 is edited'
            assert response.json['id'] == 1
            assert len(self.session.query(Message).all()) == 2

            when('The message not exists', url_parameters=Update(id=3))
            assert status == '614 Message Not Found'

            when(
                'Trying to pass using invalid message id',
                url_parameters=Update(id='Invalid')
            )
            assert status == '707 Invalid MessageId'

            when(
                'Try to send long text',
                form=Update(body=(1024 + 1) * 'a')
            )
            assert status == '702 Must be less than 1024 charecters'

    # TODO: More test scenarios should be checked when other
    # Authorizations would be implemented
    def test_forbidden_request(self):
        self.login('user2@example.com')

        with cas_mockup_server(), self.given(
            'Not allowed to edit the message',
            '/apiv1/messages/id:1/',
            'EDIT',
            form=dict(body='Message 1 should not be edited')
         ):
             assert status == 403

             when('Try to pass an unauthorized request', authorization=None)
             assert status == 401

