from bddrest.authoring import given, when, status, response, Update, Remove

from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server
from jaguar.models import User, Message, Room


class TestReplyMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session(expire_on_commit=True)
        cls.message1 = Message(
            body='This is message 1',
            mimetype='text/plain'
        )
        cls.message2 = Message(
            body='This is message 2',
            mimetype='text/plain'
        )
        user = User(
            title='user',
            email='user@example.com',
            access_token='access token',
            reference_id=1
        )
        session.add(user)
        user1 = User(
            title='user1',
            email='user1@example.com',
            access_token='access token1',
            reference_id=2,
            messages=[cls.message1, cls.message2]
        )
        cls.room = Room(
            title='room',
            messages=[cls.message1, cls.message2],
            members=[user1]
        )
        session.add(cls.room)
        cls.message2.soft_delete()
        session.commit()

    def test_reply_a_message(self):
        self.login('user@example.com')

        with cas_mockup_server(), self.given(
            f'Reply message 1',
            f'/apiv1/messages/id:{self.message1.id}',
            f'REPLY',
            form=dict(
                body='This is a reply to message1',
                mimetype='text/plain'
            )
        ):
            assert status == 200
            assert response.json['replyRoot'] == self.message1.id
            assert response.json['replyTo']['body'] == 'This is message 1'
            assert len(self.room.messages) == 3

            when('Requested message not found', url_parameters=Update(id=4))
            assert status == '614 Message Not Found'

            when(
                'Request a message with invalid message id',
                url_parameters=Update(id='message1')
            )
            assert status == '707 Invalid MessageId'

            when(
                'Try to reply with unsopported media type',
                form=Update(mimetype='video/3gpp')
            )
            assert status == 415

            when(
                'Try to send reply with long text',
                form=Update(body=(1024 + 1) * 'a')
            )
            assert status == '702 Must be less than 1024 charecters'

            when('Remove body from the form', form=Remove('body'))
            assert status == '712 Message Body Required'

            when('Remove mimetype from the form', form=Remove('mimetype'))
            assert status == '713 Message Mimetype Required'

            when(
                'Requested message is already deleted',
                url_parameters=Update(id=self.message2.id)
            )
            assert status == '616 Message Already Deleted'

            when('Try to pass an unauthorized request', authorization=None)
            assert status == 401

