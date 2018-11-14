from bddrest.authoring import when, status, response, Update

from jaguar.models import Member, Room, Message
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestDeleteMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        cls.session = cls.create_session(expire_on_commit=True)
        message1 = Message(body='This is message 1', mimetype='text/plain')
        message2 = Message(body='This is message 2', mimetype='text/plain')
        user1 = Member(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2,
            messages=[message1, message2]
        )
        user2 = Member(
            email='user2@example.com',
            title='user2',
            access_token='access token2',
            reference_id=3
        )
        room = Room(title='room', type='room', messages=[message1, message2])
        room.members.append(user1)
        cls.session.add(user2)
        cls.session.add(room)
        cls.session.commit()

    def test_delete_the_message(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Try to delete a message',
            '/apiv1/messages/id:1',
            'DELETE'
        ):
            assert status == 200
            assert response.json['body'] == 'This message is deleted'
            assert len(self.session.query(Message).all()) == 2
            message1 = self.session.query(Message) \
                .filter(Message.id == 1) \
                .one()
            assert message1.body == 'This message is deleted'
            assert message1.is_deleted == True

            when('Delete the same message')
            assert status == '616 Message Already Deleted'

            when('The message not exists', url_parameters=Update(id=3))
            assert status == '614 Message Not Found'

            when(
                'Trying to pass using invalid message id',
                url_parameters=Update(id='Invalid')
            )
            assert status == '707 Invalid MessageId'

    # TODO: More test scenarios should be checked when other
    # Authorizations would be implemented
    def test_forbidden_request(self):
        self.login('user2@example.com')

        with cas_mockup_server(), self.given(
            'Not allowed to delete the message',
            '/apiv1/messages/id:2/',
            'DELETE',
        ):
            assert status == 403

